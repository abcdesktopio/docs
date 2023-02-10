
# IPC and pod


Does a pod can share memory between his container ?
Does Posix shared memory work with containers ? 
Does System V shared memory work with containers ? 

Let's have a look !

There are two ways to use shared memory in Linux:  `System V ` and  `POSIX `.

* `shmget` / `shmat` / `shmdt` for the  `System V ` method.
* `shm_open` / `mmap` / `shm_unlink` for the  `POSIX ` method.



## Requirements


- `kubectl` command-line tool must be configured to communicate with your cluster. 


## Install the bash and yaml files

To install the bash and yaml files, run the command

```
git clone https://github.com/abcdesktopio/podshmtest.git
cd podshmtest
```

## Shared memory

### System V shared memory

Goal: Test `System V shared memory` between two containers inside the same pod

This test creates two containers a sender and a receiver. The sender writes a string in a share memory and the receiver read the string.

The test is successful if there is no system error and the strings are equals.

The string MemContents stored in the shared memory is : This is the way the world ends...

* The sender container writes a string from stdin into shared memory. The source code is [here](https://github.com/abcdesktopio/podshmtest/tree/main/src/sysv)

``` c
    int exit_code = -1;
    // ftok to generate unique key 
    key_t key = ftok("/shared/shmfile",65);
    // shmget returns an identifier in shmid 
    int shmid = shmget(key,1024,0666|IPC_CREAT);
    // shmat to attach to shared memory 
    char *str = (char*) shmat(shmid,(void*)0,0);
    strcpy( str, MemContents );
    //detach from shared memory  
    exit_code = shmdt(str);
```

* The receiver container print the sender's shared memory string to stdout. The source code is [here](https://github.com/abcdesktopio/podshmtest/tree/main/src/sysv)


``` c
    // ftok to generate unique key 
    key_t key = ftok("/shared/shmfile",65);
    // shmget returns an identifier in shmid 
    int shmid = shmget(key,1024,0666|IPC_CREAT);
    // shmat to attach to shared memory 
    char *str = (char*) shmat(shmid,(void*)0,0);
    printf("%s\n",str);
    cmp_code = strcmp( str, MemContents );
    //detach from shared memory  
    exit_code = shmdt(str);
```

To run the `System V` tests

### Run a shared memory test access using a shared path

In this yaml file, sender and receiver containers share a file. This file is
`/shared/me` and it is the first parameter to `ftok` system V call. 

```
apiVersion: v1
kind: Pod
metadata:
  name: podsysvsendershmtest
spec:
  shareProcessNamespace: true
  restartPolicy : Never
  volumes:
    - name: shared 
      emptyDir: {}
  containers:
    - name: sender
      imagePullPolicy: IfNotPresent
      image: abcdesktopio/ipctest
      command: [ "/bin/sleep", "1d" ]
      volumeMounts:
      - name: shared
        mountPath: /shared
      env:
      - name: FTOK_PATH
        value: "/shared/me"
    - name: receiver
      imagePullPolicy: IfNotPresent
      image: abcdesktopio/ipctest
      command: [ "/bin/sleep", "1d" ]
      volumeMounts:
      - name: shared
        mountPath: /shared
      env:
      - name: FTOK_PATH
        value: "/shared/me"
```

> The env var `FTOK_PATH` set the first parameter to `ftok` system V call.


Run the test 

``` bash
# this test result is success
./runtest.sh podsendershared_success.yaml
```

You can read the same string from sender to receive container. 

**This test is OK.**

```
pod/podsysvsendershmtest created
pod/podsysvsendershmtest condition met
**** Start sender ****
sender starts
identity of the file named FTOK_PATH=/shared/me
sending success This is the way the world ends...
**** Read on receiver **** 
receive starts
identity of the file named FTOK_PATH=/shared/me
read This is the way the world ends...
```





### Run a shared memory test access without shared path


In this yaml file, sender and receiver do not share file.
`/dummy` filename is the first parameter to `ftok` system V call. 



``` yaml
apiVersion: v1
kind: Pod
metadata:
  name: podsysvsendershmtest
spec:
  shareProcessNamespace: true
  restartPolicy : Never
  volumes:
    - name: shared 
      emptyDir: {}
  containers:
    - name: sender
      imagePullPolicy: IfNotPresent
      image: abcdesktopio/ipctest
      command: [ "/bin/sleep", "1d" ]
      volumeMounts:
      - name: shared
        mountPath: /shared
      env:
      - name: FTOK_PATH
        value: "/dummy"
    - name: receiver
      imagePullPolicy: IfNotPresent
      image: abcdesktopio/ipctest
      command: [ "/bin/sleep", "1d" ]
      volumeMounts:
      - name: shared
        mountPath: /shared
      env:
      - name: FTOK_PATH
        value: "/dummy"
```

> The env var `FTOK_PATH` set the first parameter to `ftok` system V call.

Run the test 

``` bash
# this test result is failed
./runtest.sh podsendershared_failed.yaml
```

You can read that the sender write a string.
The receiver does not read this string. 

**This test is KO.**

```
pod "podsysvsendershmtest" deleted
pod/podsysvsendershmtest created
pod/podsysvsendershmtest condition met
**** Start sender ****
sender starts
identity of the file named FTOK_PATH=/dummy
sending success This is the way the world ends...
**** Read on receiver **** 
receive starts
identity of the file named FTOK_PATH=/dummy
main: ftok() for shm failed
this is an unlimited loop, waiting 5s
receive starts
identity of the file named FTOK_PATH=/dummy
main: ftok() for shm failed
this is an unlimited loop, waiting 5s
receive starts
identity of the file named FTOK_PATH=/dummy
main: ftok() for shm failed
this is an unlimited loop, waiting 5s
...
^C
command terminated with exit code 130
```


> The [ftok](https://man7.org/linux/man-pages/man3/ftok.3.html)() function uses the identity of the file named by the given pathname (which must refer to an existing, accessible file)
> The file named by the given pathname must be shared by using a volume between containers






### POSIX shared memory

Goal: Test `Posix shared memory` between two containers inside the same pod

The source code is from inter-process communication in Linux:
[Shared storage
Learn how processes synchronize with each other in Linux](https://opensource.com/article/19/4/interprocess-communication-linux-storage)
. The author is [Marty Kalin](https://opensource.com/users/mkalindepauledu)

This test creates two containers a sender and a receiver to read a shared memory in `/dev/shm`, it uses a semaphore as a mutex (lock) by waiting for writer to increment it.

The string `MemContents` stored in the shared memory is : `This is the way the world ends...`

* The sender container writes a string into shared memory map file `/shMemEx`

``` c
  int fd = shm_open(BackingFile,      /* name from smem.h */
                    O_RDWR | O_CREAT, /* read/write, create if needed */
                    AccessPerms);     /* access permissions (0644) */
  if (fd < 0) report_and_exit("Can't open shared mem segment...");

  ftruncate(fd, ByteSize); /* get the bytes */

  caddr_t memptr = mmap(NULL,       /* let system pick where to put segment */
                        ByteSize,   /* how many bytes */
                        PROT_READ | PROT_WRITE, /* access protections */
                        MAP_SHARED, /* mapping visible to other processes */
                        fd,         /* file descriptor */
                        0);         /* offset: start at 1st byte */
  if ((caddr_t) -1  == memptr) report_and_exit("Can't get segment...");

  fprintf(stderr, "shared mem address: %p [0..%d]\n", memptr, ByteSize - 1);
  fprintf(stderr, "backing file:       /dev/shm%s\n", BackingFile );

  /* semahore code to lock the shared mem */
  sem_t* semptr = sem_open(SemaphoreName, /* name */
                           O_CREAT,       /* create the semaphore */
                           AccessPerms,   /* protection perms */
                           0);            /* initial value */
  if (semptr == (void*) -1) report_and_exit("sem_open");

  strcpy(memptr, MemContents); /* copy some ASCII bytes to the segment */

  /* increment the semaphore so that memreader can read */
  if (sem_post(semptr) < 0) report_and_exit("sem_post");

  sleep(12); /* give reader a chance */

  /* clean up */
  munmap(memptr, ByteSize); /* unmap the storage */
  close(fd);
  sem_close(semptr);
  shm_unlink(BackingFile); /* unlink from the backing file */

```

* The receiver container print the sender's shared memory string to stdout


``` c
  int fd = shm_open(BackingFile, O_RDWR, AccessPerms);  /* empty to begin */
  if (fd < 0) report_and_exit("Can't get file descriptor...");

  /* get a pointer to memory */
  caddr_t memptr = mmap(NULL,       /* let system pick where to put segment */
                        ByteSize,   /* how many bytes */
                        PROT_READ | PROT_WRITE, /* access protections */
                        MAP_SHARED, /* mapping visible to other processes */
                        fd,         /* file descriptor */
                        0);         /* offset: start at 1st byte */
  if ((caddr_t) -1 == memptr) report_and_exit("Can't access segment...");

  /* create a semaphore for mutual exclusion */
  sem_t* semptr = sem_open(SemaphoreName, /* name */
                           O_CREAT,       /* create the semaphore */
                           AccessPerms,   /* protection perms */
                           0);            /* initial value */
  if (semptr == (void*) -1) report_and_exit("sem_open");
  
  /* use semaphore as a mutex (lock) by waiting for writer to increment it */
  if (!sem_wait(semptr)) { /* wait until semaphore != 0 */
    int i;
    for (i = 0; i < strlen(MemContents); i++)
      write(STDOUT_FILENO, memptr + i, 1); /* one byte at a time */
    sem_post(semptr);
  }
  
  /* cleanup */
  munmap(memptr, ByteSize);
  close(fd);
  sem_close(semptr);
  unlink(BackingFile);
```



To run the `POSIX` test

```
kubectl create -f https://raw.githubusercontent.com/abcdesktopio/podshmtest/main/podposixshm.yaml 
pod/podposixshm created
```


The `podposixshm` pod status must be `Completed`

```
kubectl get pods podposixshm  
NAME          READY   STATUS      RESTARTS   AGE
podposixshm   0/2     Completed   0          27s
```


The podposixshm sender log file should be :

```
kubectl logs pod/podposixshm sender
shared mem address: 0x7fc0ea582000 [0..511]
backing file:       /dev/shm/shMemEx
```

The pod/podposixshm receiver log file should be :

```
kubectl logs pod/podposixshm receiver
This is the way the world ends...
```



Delete the `podposixshm` pod 

```
kubectl delete pods podposixshm 
pod "podposixshm" deleted
```



## Read the shared memory default limit


On a pod, we can see that the default size of `/dev/shm` is 64MB, when running the `df /dev/shm` command.


``` bash
kubectl run -it --image alpine:edge shmtest -- sh
If you don't see a command prompt, try pressing enter.
```

``` bash
df /dev/shm
Filesystem           1K-blocks      Used Available Use% Mounted on
shm                      65536     65536         0 100% /dev/shm
``` 

A `dd` command confirm this limit. it will throw an exception when it reaches 64MB: “No space left on device”.


Run the `dd` command


``` bash
dd if=/dev/zero of=/dev/shm/test
dd: error writing '/dev/shm/test': No space left on device
131073+0 records in
131072+0 records out
```

Run the `df /dev/shm` command

```
df /dev/shm
Filesystem           1K-blocks      Used Available Use% Mounted on
shm                      65536     65536         0 100% /dev/shm
```

Delete the `shmtest` pod

``` bash
kubectl delete pods shmtest
pod "shmtest" deleted
```

> The default size is 64 MB.



## Increase the shared memory default limit


Create a `updateshm.yaml` file with the yaml content 

```
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: updateshm
  name: updateshm
spec:
  volumes:                          
    - name: volumeshm
      emptyDir:
        medium: Memory
  containers:
  - image: alpine:edge
    name: updateshm
    args: 
      - 1d 
    command: 
      - /bin/sleep
    volumeMounts:                 
        - mountPath: /dev/shm
          name: volumeshm
  dnsPolicy: ClusterFirst
  restartPolicy: Never
```

Create the new pod `updateshm`

```
kubectl apply -f updateshm.yaml 
pod/updateshm created
```

Execute a `df /dev/shm` command inside this pods to read the size of `/dev/shm`

```
kubectl exec updateshm -- df /dev/shm
Filesystem           1K-blocks      Used Available Use% Mounted on
tmpfs                 16176264         0  16176264   0% /dev/shm
```

The size of `/dev/shm` is 16176264 of 1K blocks. The new default size is 16 GB.


To set a fixed limit use the `sizeLimit` in the `spec.volumes`

```
apiVersion: v1
kind: Pod
metadata:
  labels:
    run: updateshm512
  name: updateshm512
spec:
  volumes:                          
    - name: updateshm512
      emptyDir:
        medium: Memory
        sizeLimit: 512Mi
  containers:
  - image: alpine:edge
    name: updateshm
    args: 
      - 1d 
    command: 
      - /bin/sleep
    volumeMounts:                 
        - mountPath: /dev/shm
          name: updateshm512
  dnsPolicy: ClusterFirst
  restartPolicy: Never
```

