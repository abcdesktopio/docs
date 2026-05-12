
## Contribute to abcdesktop community

Please note some rules to apply for all contributions:

??? success must "Everything must be in github"
    To ensure consistency, collaboration, and easy access for our community members working on abcdesktop, all projects related to feature development must be hosted within github. By keeping everything under one roof, we can:

    1. Facilitate collaboration among developers: By hosting all feature development projects in a centralized location like Github, it becomes easier for team members and contributors to
    work together on various aspects of the features. This promotes efficient communication and faster problem-solving.
    2. Keep things organized: Having all features development projects in one place makes it simpler to navigate and manage our Git repositories. This helps maintain a clean and
    well-structured codebase that is easier for both newcomers and experienced developers to work with.
    3. Enforce best practices: By requiring all feature development projects to be hosted within Github, we can enforce consistent coding standards and best practices across the board.
    This ensures that all features are developed in a uniform manner, making it easier to maintain and update them over time.
    4. Encourage code reviews: Github allows for easy code review and collaboration, which helps catch potential issues early on and improve the overall quality of our features. By
    requiring all feature development projects to be hosted within Github, we can ensure that every change undergoes thorough scrutiny before being merged into the main branch.
    5. Provide easy access to resources: Hosting all feature development projects in Github allows us to easily share documentation, wiki pages, and other resources with our community
    members. This makes it simpler for developers to find the information they need to contribute effectively to the project.
    6. Improve security: By centralizing our feature development efforts within Github, we can better monitor and control access to sensitive data and code. This helps maintain a high
    level of security for our features and reduces the risk of unauthorized changes or breaches.
    7. Simplify project management: Having all feature development projects in Github makes it easier for us to track progress, manage issues, and release updates more efficiently. This
    leads to faster turnaround times and happier users.

    By requiring all abcdesktop feature development projects to be hosted within Github, we can streamline our development process, encourage collaboration, and improve the overall
    quality of features for our community members. We appreciate your understanding and cooperation in adhering to this policy.


??? success must "Everything to be deployed must be a container image"
    1. Consistent Deployment: With abcdesktop being based on Kubernetes, requiring everything to be deployed as a container image ensures that deployments are consistent across different environments and platforms. Container images provide a standardized way of packaging applications and their dependencies, making it easier to manage and scale deployments within the abcdesktop ecosystem.

    2. Improved Portability: Containers are platform-agnostic, meaning they can run on any operating system that supports container runtime engines like Kubernetes. This portability enables rapid deployment and easy migration between environments within the abcdesktop ecosystem, reducing the risk of compatibility issues and improving development agility.

    3. Enhanced Security: Container images provide a secure sandboxed environment for applications, isolating them from the host system and other containers. This isolation helps mitigate potential security risks by preventing unauthorized access and malware infiltration within the abcdesktop ecosystem.

    4. Simplified Configuration: With container images, configurations are declarative and standardized, making it easier to manage and version deployments within the abcdesktop ecosystem. This simplification reduces the risk of configuration errors and ensures that deployments remain consistent over time.

    5. Scalability and Resource Optimization: Containers are highly scalable as they can be easily orchestrated by Kubernetes to allocate resources efficiently across multiple nodes within the abcdesktop ecosystem. This efficient use of resources leads to cost savings, improved performance, and better reliability for deployments within the ecosystem.

    6. Automated Deployment: Container images facilitate automated deployment through tools like Helm and Kustomize. These tools automate the process of creating, managing, and deploying containerized applications, reducing the risk of human error and improving deployment speed within the abcdesktop ecosystem.

    7. Easier Testing and Development: Containers make it easier to create isolated testing environments that closely mirror production environments within the abcdesktop ecosystem. This improved testing environment leads to more robust applications and faster development cycles, helping to accelerate innovation within the ecosystem.


??? success must "Container image content must not be run as root"
    1. Enhanced Security: Running container image content without root privileges reduces the risk of unauthorized access or malicious activities within the container and the host system. By limiting the level of privilege, you minimize potential security vulnerabilities and limit the impact of any breaches that may occur.

    2. Least Privilege Principle: The least privilege principle states that a process should be given the minimum set of permissions necessary to complete its intended function. By running container image content without root privileges, you adhere to this principle, further enhancing overall system security.

    3. Containment and Isolation: By restricting the level of privilege, you ensure that containerized applications are contained within their designated sandbox, preventing them from interfering with other containers or the host system. This containment and isolation help maintain system stability and reduce the risk of unintended interactions between components.

    4. Reduced Attack Surface: By running container image content without root privileges, you reduce the attack surface of your system, making it more difficult for malicious actors to exploit vulnerabilities or gain access to sensitive data. This reduced attack surface helps maintain a secure environment within the Kubernetes ecosystem.

    5. Simplified Security Management: Without the need to manage root permissions for each containerized application, you simplify security management and reduce the complexity of maintaining a secure environment. This simplification makes it easier to implement and enforce security best practices across the entire Kubernetes ecosystem.

    6. Compliance with Best Practices: By adhering to the principle of running container image content without root privileges, you align your Kubernetes deployment with industry best practices and security guidelines, further enhancing the overall security posture of your system.

??? success must "Every container image must be public"
    To be sure all core features are available to everyone, we require that every container image used by abcdesktop is publicly accessible.

    1. Enhanced Collaboration and Sharing: By making all Docker images used by abcdesktop public, developers can easily share their work with others in the community. This encourages collaboration, as others can use, modify, and contribute back to these open-source projects.
    2. Increased Transparency: When Docker images are open-source, users have full visibility into what they're deploying. This transparency allows for more informed decisions regarding security and compatibility with existing systems.
    3. Security Vulnerabilities Mitigation: Public Docker images often receive scrutiny from a larger community of developers. By making all images public, you increase the likelihood that any potential security vulnerabilities will be discovered and addresse
    4. Improved Reusability: By using public Docker images, developers can leverage best practices and industry-standard configurations that have been tested by others. This can help improve the quality and reliability of deployed applications.
    5. Compliance with Open Source Philosophy: Many organizations embrace open source philosophies. Making all Docker images used by a Helm public aligns with these values, fostering an atmosphere of collaboration, innovation, and shared knowledge.
    6. Accelerated Development Cycle: By using established and well-documented public Docker images, developers can focus more on their application logic rather than spending time on setting up infrastructure and configuring base images. This accelerates the development cycle and reduces time to market.

??? success should "Every feature should be in Github abcdesktop organisation"
    To facilitate collaboration and ensure efficient development of abcdesktop features, we recommend that all abcdesktop feature projects be hosted in the abcdesktop Github organisation for working on individual tasks and features. By hosting all feature projects within the abcdesktop Github organisation, you will benefit from several advantages:

    1. Collaboration: The Github group allows multiple developers to work together on a single project simultaneously, enabling efficient collaboration and reducing redundant effort.
    2. Version Control: Github provides version control for all projects, allowing developers to track changes made to the codebase and easily revert to previous versions if necessary.
    3. Issues & Milestones: The Github group allows users to create issues and milestones for each project, enabling clear communication regarding what needs to be done and when.
    4. Merge Requests: The Github group facilitates the creation of merge requests for code changes, allowing developers to easily propose their changes and collaborate on improvements
    with other team members.
    5. Code Reviews: The Github group allows for code reviews of submitted changes, ensuring that all code adheres to our coding standards and best practices.
    6. Accessibility: By hosting all feature projects within the YourDev Github group, we ensure that all developers have access to the latest code and can contribute effectively to the
    project.
    7. Documentation: The Github group allows for clear documentation of each project, including README files, CONTRIBUTING guides, and other relevant information.
    8. Integration with Other Tools: The Github group integrates seamlessly with other tools commonly used by developers, such as Jenkins, Travis CI, and Docker, enabling efficient
    Continuous Integration (CI) and Continuous Deployment (CD).

    By following this recommendation, we encourage developers to collaborate effectively, reduce redundancy, and streamline the development process for abcdesktop feature projects. We
    believe that by using Github as our primary platform for managing feature projects, we can ensure a high-quality experience for all users of the abcdesktop operating system.

??? success could "Feature can be done with any programming language"
    1. Flexibility in Development: Allowing developers to use any programming language for features within Docker images provides flexibility and encourages innovation. Developers can choose the tools they are most comfortable with, leading to more efficient development processes.
    2. Community Support: By supporting multiple programming languages, you tap into a wider developer community, as different communities tend to favor specific languages. This increased support can lead to faster resolution of issues, improved documentation, and more contributions from diverse developers.
    3. Technological Advancements: Allowing for the use of various programming languages ensures that projects can take advantage of technological advancements in multiple languages. This adaptability helps keep projects up-to-date with the latest development trends and best practices.
    4. Compatibility with Existing Infrastructure: By supporting multiple programming languages, you can ensure compatibility with existing infrastructure that may be written in different languages. This compatibility makes it easier to integrate new features into existing systems without having to rewrite large portions of code or introduce potential compatibility issues.
    5. Increased Developer Satisfaction: Giving developers the freedom to use their preferred programming language can lead to increased job satisfaction and productivity. By reducing friction in the development process, you encourage a more positive work environment and higher-quality contributions.
    6. Reduced Learning Curve: Allowing for multiple programming languages means that developers do not have to learn a new language just to contribute to a project. This reduced learning curve makes it easier for newcomers to join the project and contributes to a more active developer community.
    7. Avoiding Vendor Lock-In: By supporting multiple programming languages, you avoid vendor lock-in, as developers are not tied to a specific language or technology stack. This flexibility allows projects to adapt to changing needs and market trends without having to completely rewrite their codebase.

??? success must "Every bug report or support request must be done throws Github ticketing"
    1. Centralized Management: By using the single platform GitHub for all bug reports and support requests, it becomes easier to manage and track these issues in one place. This centralization makes it simpler for developers to address problems quickly and maintain the quality of their project.
    2. Increased Visibility: With a public ticketing system, other community members can view and contribute to discussions related to bug reports and support requests. This increased visibility helps foster collaboration and ensures that the most effective solutions are found.
    3. Improved Organization: A centralized ticketing system allows for better organization of issues, making it easier to prioritize and manage tasks based on their severity, impact, or dependencies. This improved organization can lead to more efficient resolution times.
    4. Transparency and Accountability: Public ticketings foster transparency by making the entire process of resolving issues visible to the community. This accountability ensures that developers are responsive to user needs and address issues in a timely manner.
    5. Better Documentation: As more bug reports and support requests are handled through GitHub, developers can use this information to improve their documentation. Clearer, more comprehensive documentation will make it easier for newcomers to contribute to the project and reduce the number of support requests in the future.
    6. Efficient Collaboration: GitHub makes it easy for team members to collaborate on issues, with features like comments, discussions, and code changes directly within the ticket. This collaboration streamlines the resolution process, helping teams work together more effectively.
    7. Historical Record: A centralized ticketing system creates a historical record of all issues that have been reported and addressed. This can be useful for future reference when similar problems arise or when developers need to understand how previous issues were resolved.

??? success must "Every feature request must be done throws Github ticketing"
    1. Centralized Feature Requests: By using the single platform GitHub for all feature requests, it becomes easier to manage and prioritize these requests in one place. This centralization makes it simpler for developers to understand the community's needs and prioritize their work accordingly.
    2. Increased Visibility: With a public ticketing system, other community members can view and contribute to discussions related to feature requests. This increased visibility helps foster collaboration and ensures that the most beneficial features are implemented.
    3. Improved Organization: A centralized ticketing system allows for better organization of feature requests, making it easier to prioritize and manage tasks based on their impact, feasibility, or dependencies. This improved organization can lead to more efficient implementation times.
    4. Transparency and Accountability: Public ticketings foster transparency by making the entire process of implementing new features visible to the community. This accountability ensures that developers are responsive to user needs and implement features in a timely manner.
    5. Better Prioritization: By having all feature requests centralized, developers can easily see which features have the most support or are most requested by the community. This helps them prioritize their work effectively and focus on delivering the features that will be most beneficial to users.
    6. Community Engagement: A centralized ticketing system encourages community engagement by allowing users to propose and discuss new features directly with developers. This collaboration can lead to innovative solutions and a more tailored product that better meets user needs.
    7. Historical Record: A centralized ticketing system creates a historical record of all feature requests that have been made and implemented. This can be useful for future reference when similar ideas arise or when developers need to understand how previous features were conceived and developed.

??? success must "Every feature contribution must be done throws Github merge request"
    1. Centralized Contributions: By using the single platform GitHub for all feature contributions, it becomes easier to manage and review these contributions in one place. This centralization makes it simpler for developers to understand the community's work and ensure that changes align with project goals.
    2. Increased Collaboration: GitHub merge requests allow multiple team members to collaborate on a single contribution, providing feedback, suggestions, or code reviews before the feature is merged into the main branch. This collaboration helps maintain high-quality code and ensures that features are well-tested and thoroughly vetted.
    3. Improved Organization: Centralized merge requests allow for better organization of contributions, making it easier to track the progress of each contribution and manage tasks based on their status (open, in progress, or merged). This improved organization can lead to more efficient development cycles.
    4. Transparency and Accountability: GitHub provides a transparent record of all changes made to the project, with detailed commit messages and merge request discussions. This transparency ensures that developers are accountable for their contributions and promotes a culture of continuous improvement.
    5. Code Review Best Practices: By using GitHub merge requests, contributors can follow best practices for code reviews, including conducting peer-to-peer reviews, addressing feedback, and ensuring that changes adhere to the project's coding standards. This helps maintain high-quality code and promotes a consistent development style.
    6. Faster Feedback Loop: GitHub merge requests enable developers to quickly provide feedback on contributions, reducing the time between submission and review. This faster feedback loop encourages frequent updates and ensures that features are developed efficiently.
    7. Historical Record: A centralized system for feature contributions creates a historical record of all changes made to the project. This can be useful for future reference when similar ideas arise or when developers need to understand how previous features were implemented and refined over time.

## Contribute to this documentation

This section outlines the guidelines for contributing to the Documentation of abcdesktop. By following these rules, you can help create a helpful, accurate, and user-friendly resource that assists others in using and troubleshooting abcdesktop effectively.

??? success must "All documentation is managed inside the [documentation github project](https://github.com/abcdesktopio/newdocs)"
    Documentation is generated from Github, any other way to update it will be override.

??? success must "Documentation must be in english"
    Using a single language helps maintain consistency across all pages of the documentation. This makes it easier for users to navigate and understand the content, as they don't have to switch between multiple languages or interpret translations.

??? success must  "Contributions must be done throws merge requests"
    This ensures that all changes are reviewed and approved by the maintainers before being merged into the main branch. This helps maintain the quality and consistency of the documentation.

### Markdown instructions



####  Graphical

- Use `mermaid` or `drawio` if you can, text format is always better than binary.
- If you can't put the original file as the same name but with other extension to allow changes for others

#### NAMESPACE for command line

Use `NAMESPACE` as a variable

```
NAMESPACE=abcdesktop
kubectl apply -f http-router.yaml -n abcdesktop
```

Do not set the abcdesktop namespace as the namepsace in `kubectl` command line

```
kubectl apply -f http-router.yaml -n abcdesktop
```




