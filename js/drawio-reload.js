(function () {
  var loaded = false;

  function renderDiagrams() {
    GraphViewer.processElements();
  }

  function loadViewerScript(callback) {
    if (loaded) { callback(); return; }
    var s = document.createElement('script');
    s.src = 'https://viewer.diagrams.net/js/viewer-static.min.js';
    s.onload = function () { loaded = true; callback(); };
    document.head.appendChild(s);
  }

  document$.subscribe(function (_ref) {
    var body = _ref.body;
    if (body.querySelector('.mxgraph, [data-mxgraph]')) {
      loadViewerScript(renderDiagrams);
    }
  });
})();