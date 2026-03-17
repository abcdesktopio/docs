/**
 * wizard.js
 *
 * Two responsibilities, coordinated in a single module:
 *
 * 1. WIZARD STATE  — persists the active tabs across wizard pages
 *      wiz-profile  — active profile : admin | developer | user
 *      wiz-process  — active process tab : Manuel / Script / Helm
 *      wiz-os       — active OS sub-tab  : Linux/macOS | Windows
 *
 * 2. TOC TAB FILTER — hides TOC entries that belong to inactive tabs
 *      Reads data-tab-path attributes injected by hooks/toc_tab_filter.py
 *      filterToc() is called AFTER restore() so the TOC reflects the
 *      restored tab state, not the default one.
 *
 * HTML structure produced by pymdownx.tabbed alternate_style: true
 *
 *   <div class="tabbed-set tabbed-alternate" data-tabs="1:3">
 *     <input checked id="__tabbed_1_1" name="__tabbed_1" type="radio">
 *     <input id="__tabbed_1_2" ...>
 *     <div class="tabbed-labels">
 *       <label for="__tabbed_1_1">Manuel</label>
 *       <label for="__tabbed_1_2">Script</label>
 *     </div>
 *     <div class="tabbed-content">
 *       <div class="tabbed-block"> ... </div>
 *       <div class="tabbed-block">
 *         <div class="tabbed-set tabbed-alternate" data-tabs="2:2"> ... </div>
 *       </div>
 *     </div>
 *   </div>
 *
 * Bug fixes vs previous versions:
 *   1. querySelector(":scope > input:checked") is unreliable on direct-child
 *      <input> elements — replaced by iterating tabbedSet.children.
 *   2. isPathActive() rule `tabPath.startsWith(active+"|")` was removed:
 *      it made "Script|Windows" visible when only "Script" was active,
 *      because "Script|Windows".startsWith("Script|") is true.
 *      A sub-tab heading is only visible when its FULL path is active.
 */

(function () {
  "use strict";

  /* ================================================================
     PART 1 — WIZARD STATE
     ================================================================ */

  const KEY_PROFILE = "wiz-profile";
  const KEY_PROCESS = "wiz-process";
  const KEY_OS      = "wiz-os";

  function getProcessLabels() {
    const sets = document.querySelectorAll(".tabbed-set");
    if (!sets.length) return [];
    return sets[0].querySelectorAll(":scope > .tabbed-labels > label");
  }

  function getOSLabels() {
    const nested = document.querySelectorAll(".tabbed-set .tabbed-set");
    if (!nested.length) return [];
    return nested[0].querySelectorAll(":scope > .tabbed-labels > label");
  }

  function activateByText(labels, text) {
    if (!text) return false;
    for (const label of labels) {
      if (label.textContent.trim() === text) {
        label.click();
        return true;
      }
    }
    return false;
  }

  function getPageProfile() {
    const meta = document.querySelector('meta[name="wiz-profile"]');
    return meta ? meta.getAttribute("content") : null;
  }

  function restoreOverviewTab() {
    const saved = localStorage.getItem(KEY_PROFILE);
    if (!saved) return;
    const labels = document.querySelectorAll(
      ".tabbed-set > .tabbed-labels > label"
    );
    for (const label of labels) {
      if (label.textContent.trim().toLowerCase().includes(saved)) {
        label.click();
        break;
      }
    }
  }

  function bindSave() {
    getProcessLabels().forEach((label) => {
      label.addEventListener("click", () => {
        localStorage.setItem(KEY_PROCESS, label.textContent.trim());
      });
    });

    getOSLabels().forEach((label) => {
      label.addEventListener("click", () => {
        localStorage.setItem(KEY_OS, label.textContent.trim());
      });
    });

    const isOverview = document.querySelector('meta[name="wiz-overview"]');
    if (isOverview) {
      document
        .querySelectorAll(".tabbed-set > .tabbed-labels > label")
        .forEach((label) => {
          label.addEventListener("click", () => {
            localStorage.setItem(
              KEY_PROFILE,
              label.textContent.trim().toLowerCase().replace(/[^a-z]/g, "")
            );
          });
        });
    }
  }

  function restore() {
    const isOverview = document.querySelector('meta[name="wiz-overview"]');

    if (isOverview) {
      restoreOverviewTab();
      filterToc();
      return;
    }

    const pageProfile = getPageProfile();
    if (pageProfile) {
      localStorage.setItem(KEY_PROFILE, pageProfile);
    }

    activateByText(getProcessLabels(), localStorage.getItem(KEY_PROCESS));
    filterToc();

    const savedOS = localStorage.getItem(KEY_OS);
    if (savedOS) {
      setTimeout(() => {
        activateByText(getOSLabels(), savedOS);
        filterToc();
      }, 60);
    }
  }

  /* ================================================================
     PART 2 — TOC TAB FILTER
     ================================================================ */

  /**
   * Returns the checked <input> that is a DIRECT child of tabbedSet.
   *
   * Why not querySelector(":scope > input:checked") ?
   * That CSS selector is unreliable on inline <input> elements that are
   * direct children of a <div> in some browsers / DOM implementations.
   * Iterating .children is always correct.
   */
  function getCheckedInput(tabbedSet) {
    for (const child of tabbedSet.children) {
      if (child.tagName === "INPUT" && child.checked) return child;
    }
    return null;
  }

  /**
   * Returns the label text of the active tab for a given tabbed-set.
   * Looks for the <label for="id"> inside :scope > .tabbed-labels
   * to avoid matching labels from nested sets.
   */
  function getActiveLabel(tabbedSet) {
    const input = getCheckedInput(tabbedSet);
    if (!input) return null;
    const label = tabbedSet.querySelector(
      `:scope > .tabbed-labels > label[for="${input.id}"]`
    );
    return label ? label.textContent.trim() : null;
  }

  /**
   * Walks up the DOM from a tabbed-set and builds the ancestor path
   * "GrandParent|Parent" by finding each enclosing tabbed-block
   * and the active label of its parent tabbed-set.
   */
  function getAncestorPath(tabbedSet) {
    const parts = [];
    let node = tabbedSet.parentElement;

    while (node) {
      if (node.classList.contains("tabbed-block")) {
        // node.parentElement         = .tabbed-content
        // node.parentElement.parentElement = .tabbed-set (the enclosing set)
        const parentContent = node.parentElement;
        const parentSet = parentContent && parentContent.parentElement;
        if (parentSet && parentSet.classList.contains("tabbed-set")) {
          const label = getActiveLabel(parentSet);
          if (label) parts.unshift(label);
        }
      }
      node = node.parentElement;
    }
    return parts.join("|");
  }

  /**
   * Returns a Set of all currently active full paths.
   *
   * Example when "Script" > "Linux or MacOs" is active:
   *   { "Script", "Script|Linux or MacOs" }
   *
   * "Script" is included because set1 (top-level) has "Script" checked.
   * "Script|Linux or MacOs" is included because set2 (nested) has
   * "Linux or MacOs" checked and its ancestor is "Script".
   */
  function getActivePaths() {
    const paths = new Set();

    document.querySelectorAll(".tabbed-set").forEach(function (set) {
      const label = getActiveLabel(set);
      if (!label) return;
      const ancestor = getAncestorPath(set);
      paths.add(ancestor ? ancestor + "|" + label : label);
    });

    return paths;
  }

  /**
   * Returns true if the heading's tabPath should be visible.
   *
   * Rules:
   *   active === tabPath          → exact match, visible
   *   active.startsWith(tabPath+"|") → active is a child of tabPath
   *                                    (show the parent heading too)
   *
   * NOTE: the rule `tabPath.startsWith(active+"|")` is intentionally
   * ABSENT. Without it, "Script|Windows" is NOT shown when only
   * "Script|Linux or MacOs" is active — which is the correct behaviour.
   */
  function isPathActive(tabPath, activePaths) {
    for (const active of activePaths) {
      if (
        active === tabPath ||
        active.startsWith(tabPath + "|")
      ) {
        return true;
      }
    }
    return false;
  }

  /**
   * Shows/hides TOC entries based on the active tab state.
   * Headings without data-tab-path are always visible (outside any tab).
   */
  function filterToc() {
    const activePaths = getActivePaths();

    document
      .querySelectorAll(".md-nav--secondary .md-nav__item")
      .forEach(function (item) {
        const link = item.querySelector(":scope > .md-nav__link");
        if (!link) return;

        const id = (link.getAttribute("href") || "").replace("#", "");
        if (!id) return;

        const heading = document.getElementById(id);
        if (!heading) return;

        const tabPath = heading.getAttribute("data-tab-path");

        if (!tabPath) {
          item.style.display = "";            // outside any tab → always visible
        } else {
          item.style.display = isPathActive(tabPath, activePaths) ? "" : "none";
        }
      });
  }

  /* ================================================================
     PART 3 — INIT
     ================================================================ */

  function init() {
    restore();
    bindSave();

    // Re-filter TOC on every manual tab click
    document.querySelectorAll(".tabbed-set > input").forEach(function (input) {
      input.addEventListener("change", filterToc);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  // MkDocs Material instant navigation (SPA)
  document.addEventListener("DOMContentSwitch", init);

})();