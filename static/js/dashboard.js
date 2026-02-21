/**
 * Dashboard
 */

'use strict';

document.addEventListener('DOMContentLoaded', function (e) {
  /**
   * Data from Django
   */
  const dataElement = document.getElementById("dashboard-data");
  if (!dataElement) return;

  const dashboardData = JSON.parse(dataElement.textContent);
  const totalAssetValue = dashboardData.total_asset_value;
  const arrowStarIcon = dashboardData.arrow_star_icon;

  const themeToggle = document.getElementById("theme-toggle");
  const themeIcon = themeToggle.querySelector("i");
  const root = document.documentElement;

  const savedTheme = localStorage.getItem("theme");
  if (savedTheme) {
    root.setAttribute("data-theme", savedTheme);
    updateIcon(savedTheme);
  }

  themeToggle.addEventListener("click", () => {
    const currentTheme = root.getAttribute("data-theme") || "light";
    const newTheme = currentTheme === "light" ? "dark" : "light"

    this.location.reload()

    root.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    updateIcon(newTheme);
  });

  function updateIcon(theme) {
    if (theme === "dark") {
      themeIcon.classList.remove("bx-sun");
      themeIcon.classList.add("bx-moon");
    } else {
      themeIcon.classList.remove("bx-moon");
      themeIcon.classList.add("bx-sun");
    }
  }

  /**
  * Navbar toggler when on mobile/tablet
  */
  const toggler = document.getElementById("navbar-toggler");
  if (toggler) {
    toggler.addEventListener("click", function () {
      document.documentElement.classList.add("layout-menu-expanded");
    });
  }

  const closeBtn = document.getElementById("navbar-close");
  if (closeBtn) {
    closeBtn.addEventListener("click", function (e) {
      e.preventDefault();
      document.documentElement.classList.remove("layout-menu-expanded");
    });
  }

  /**
  * Generic modal helper (Bootstrap-style, no Bootstrap JS plugin)
  */
  function makeModalController(modalId, opts = {}) {
    const modal = document.getElementById(modalId);
    if (!modal) return null;

    const {
      openSelector = null,
      closeSelector = ".btn-close, .btn-label-secondary, [data-modal-close]",
      onOpen = null
    } = opts;

    let backdrop = null;

    function createBackdrop() {
      backdrop = document.createElement("div");
      backdrop.className = "modal-backdrop fade";
      document.body.appendChild(backdrop);

      setTimeout(() => backdrop && backdrop.classList.add("show"), 10);
      backdrop.addEventListener("click", close);
    }

    function removeBackdrop() {
      if (!backdrop) return;
      backdrop.classList.remove("show");
      setTimeout(() => {
        if (backdrop) {
          backdrop.remove();
          backdrop = null;
        }
      }, 150);
    }

    function open(triggerEl = null) {
      if (typeof onOpen === "function") onOpen(triggerEl);

      modal.style.display = "block";
      modal.removeAttribute("aria-hidden");
      document.body.classList.add("modal-open");

      createBackdrop();
      setTimeout(() => modal.classList.add("show"), 10);
    }

    function close() {
      if (document.activeElement && modal.contains(document.activeElement)) {
        document.activeElement.blur();
      }

      modal.classList.remove("show");

      setTimeout(() => {
        modal.style.display = "none";
        modal.setAttribute("aria-hidden", "true");
      }, 150);

      document.body.classList.remove("modal-open");
      removeBackdrop();
    }

    modal.querySelectorAll(closeSelector).forEach((btn) => {
      btn.addEventListener("click", close);
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && modal.classList.contains("show")) close();
    });

    if (openSelector) {
      document.querySelectorAll(openSelector).forEach((el) => {
        el.addEventListener("click", function (e) {
          if (el.tagName.toLowerCase() === "a") e.preventDefault();
          open(el);
        });
      });
    }

    return { open, close, modal };
  }

  makeModalController("basicModal", {
    openSelector: "#openModalBtn",
    closeSelector: ".btn-close, .btn-label-secondary, [data-modal-close]"
  });

  const maintenanceForm = document.getElementById("maintenanceModalForm");
  const maintenanceTitle = document.getElementById("maintenanceModalTitle");

  const assetNameEl = document.getElementById("maintenanceAssetName");
  const assignedToEl = document.getElementById("maintenanceAssignedTo");

  makeModalController("maintenanceModal", {
    openSelector: ".open-maintenance-modal",
    closeSelector: ".btn-close, .btn-label-secondary, [data-modal-close]",
    onOpen: (triggerEl) => {
      if (!triggerEl) return;

      const action = triggerEl.getAttribute("data-action");
      const assetName = triggerEl.getAttribute("data-asset-name") || "";
      const assignedTo = triggerEl.getAttribute("data-assigned-to") || "Unassigned";

      if (maintenanceForm && action) maintenanceForm.setAttribute("action", action);

      if (maintenanceTitle) {
        maintenanceTitle.textContent = assetName
          ? `Log Repair — ${assetName}`
          : "Log Repair";
      }

      if (assetNameEl) assetNameEl.textContent = assetName || "—";
      if (assignedToEl) assignedToEl.textContent = assignedTo || "Unassigned";

      if (maintenanceForm) maintenanceForm.reset();
    }
  });

  /**
  * Dropdown JS
  */
  const dropdown = document.querySelector(".dropdown-user");
  const toggle = dropdown.querySelector(".dropdown-toggle");
  const menu = dropdown.querySelector(".dropdown-menu");

  toggle.addEventListener("click", function (e) {
    e.preventDefault();
    menu.classList.toggle("show");
  });

  document.addEventListener("click", function (e) {
    if (!dropdown.contains(e.target)) {
      menu.classList.remove("show");
    }
  });

  /**
  * ApexCharts
  */
  let cardColor,
    headingColor,
    labelColor,
    legendColor,
    shadeColor,
    borderColor,
    heatMap1,
    heatMap2,
    heatMap3,
    heatMap4,
    fontFamily;

  if (savedTheme === "dark") {
    shadeColor = 'dark';
    heatMap1 = '#333457';
    heatMap2 = '#3c3e75';
    heatMap3 = '#484b9b';
    heatMap4 = '#696cff';
    cardColor = '#312d4b';
    headingColor = 'color-mix(in sRGB, #e7e3fc 90%, #312d4b)';
    labelColor = '#7a7692';
    legendColor = '#b0acc7';
    borderColor = 'color-mix(in sRGB, #e7e3fc 12%, #312d4b)';
  } else {
    shadeColor = '';
    heatMap1 = '#ededff';
    heatMap2 = '#d5d6ff';
    heatMap3 = '#b7b9ff';
    heatMap4 = '#696cff';
    cardColor = '#fff';
    headingColor = 'color-mix(in sRGB, #2e263d 90%, #fff)';
    labelColor = '#aba8b1';
    legendColor = '#6d6777';
    borderColor = 'color-mix(in sRGB, #2e263d 12%, #fff)';
  }

  fontFamily = '"Inter", -apple-system, blinkmacsystemfont, "Segoe UI", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif'

  const chartColors = {
    donut: {
      series1: '#66C732',
      series2: '#8DE45F',
      series3: '#AAEB87',
      series4: '#E3F8D7'
    }
  };

  /**
  * ApexCharts - Asset Chart (Radial Bar Chart)
  */
  const assetStatsEl = document.querySelector('#assetStats'),
    assetStatsOptions = {
      chart: {
        height: 315,
        type: 'radialBar'
      },
      series: [100],
      labels: ['Asset'],
      plotOptions: {
        radialBar: {
          startAngle: 0,
          endAngle: 360,
          strokeWidth: '70',
          hollow: {
            margin: 50,
            size: '75%',
            image: arrowStarIcon,
            imageWidth: 65,
            imageHeight: 55,
            imageOffsetY: -35,
            imageClipped: false
          },
          track: {
            strokeWidth: '50%',
            background: borderColor
          },
          dataLabels: {
            show: true,
            name: {
              offsetY: 60,
              show: true,
              color: legendColor,
              fontSize: '15px',
              fontFamily: fontFamily
            },
            value: {
              formatter: function (val) {
                return '₱' + parseFloat(totalAssetValue).toLocaleString('en-PH', {
                  minimumFractionDigits: 2,
                  maximumFractionDigits: 2
                });
              },
              offsetY: 20,
              color: headingColor,
              fontSize: '28px',
              fontWeight: '500',
              fontFamily: fontFamily,
              show: true
            }
          }
        }
      },
      fill: {
        type: 'solid',
        colors: '#71dd37'
      },
      stroke: {
        lineCap: 'round'
      },
      states: {
        hover: {
          filter: {
            type: 'none'
          }
        },
        active: {
          filter: {
            type: 'none'
          }
        }
      }
    };
  if (typeof assetStatsEl !== undefined && assetStatsEl !== null) {
    const assetStats = new ApexCharts(assetStatsEl, assetStatsOptions);
    assetStats.render();
  }
});
