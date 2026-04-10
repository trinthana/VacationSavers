"use strict";

function qs(selector) {
    return document.querySelector(selector);
}

function qsa(selector) {
    return document.querySelectorAll(selector);
}

document.addEventListener("DOMContentLoaded", function () {
    togglemenu();
    menuclick();
    menuhrres();

    var vw = window.innerWidth;

    var tooltipTriggerList = [].slice.call(qsa('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    var popoverTriggerList = [].slice.call(qsa('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    const mobileMenu = qs(".mobile-menu");
    if (mobileMenu) {
        mobileMenu.addEventListener("click", function () {
            mobileMenu.classList.toggle("on");
        });
    }

    const mobileCollapse = qs("#mobile-collapse");
    const pcodedNavbar = qs(".pcoded-navbar");
    if (mobileCollapse && pcodedNavbar) {
        mobileCollapse.addEventListener("click", function () {
            pcodedNavbar.classList.toggle("navbar-collapsed");
        });
    }

    const searchBtn = qs(".search-btn");
    const searchClose = qs(".search-close");
    const mainSearch = qs(".main-search");
    const mainSearchInput = qs(".main-search .form-control");

    if (searchBtn && mainSearch && mainSearchInput) {
        searchBtn.addEventListener("click", function () {
            mainSearch.classList.add("open");
            mainSearchInput.style.width = "90px";
        });
    }

    if (searchClose && mainSearch && mainSearchInput) {
        searchClose.addEventListener("click", function () {
            mainSearch.classList.remove("open");
            mainSearchInput.style.width = "0px";
        });
    }

    var elem = qsa(".header-user-list .userlist-box");
    for (var j = 0; j < elem.length; j++) {
        elem[j].addEventListener("click", function () {
            const headerChat = qs(".header-chat");
            const headerUserList = qs(".header-user-list");
            if (headerChat) {
                headerChat.classList.add("open");
            }
            if (headerUserList) {
                headerUserList.classList.toggle("msg-open");
            }
        });
    }

    if (vw <= 991 && mainSearch && mainSearchInput) {
        mainSearch.classList.add("open");
        mainSearchInput.style.width = "90px";
    }

    if (vw >= 1024) {
        if (qs(".main-friend-cont")) {
            new PerfectScrollbar(".main-friend-cont", {
                wheelSpeed: 0.5,
                swipeEasing: 0,
                suppressScrollX: true,
                wheelPropagation: 1,
                minScrollbarLength: 40,
            });
        }
        if (qs(".main-chat-cont")) {
            new PerfectScrollbar(".main-chat-cont", {
                wheelSpeed: 0.5,
                swipeEasing: 0,
                suppressScrollX: true,
                wheelPropagation: 1,
                minScrollbarLength: 40,
            });
        }
    }

    if (qs(".noti-body")) {
        new PerfectScrollbar(".notification .noti-body", {
            wheelSpeed: 0.5,
            swipeEasing: 0,
            suppressScrollX: true,
            wheelPropagation: 1,
            minScrollbarLength: 40,
        });
    }

    if (pcodedNavbar && !pcodedNavbar.classList.contains("theme-horizontal")) {
        new PerfectScrollbar(".navbar-content", {
            wheelSpeed: 0.5,
            swipeEasing: 0,
            suppressScrollX: true,
            wheelPropagation: 1,
            minScrollbarLength: 40,
        });
    }

    if (pcodedNavbar && pcodedNavbar.classList.contains("theme-horizontal")) {
        rmactive();
        horizontalmenu();
    }

    setTimeout(function () {
        const loaderBg = qs(".loader-bg");
        if (loaderBg) {
            loaderBg.remove();
        }
    }, 400);
});

function horizontalmenu() {
    var vw = window.innerWidth;
    const navbar = qs(".pcoded-navbar");
    if (navbar && navbar.classList.contains("theme-horizontal")) {
        if (vw < 992) {
            navbar.classList.remove("theme-horizontal");
        }
    }
}

window.addEventListener("resize", function () {
    togglemenu();
    menuhrres();

    const navbar = qs(".pcoded-navbar");
    if (navbar && navbar.classList.contains("theme-horizontal")) {
        rmactive();
        horizontalmenu();
    }

    const body = qs("body");
    if (body && (body.classList.contains("layout-6") || body.classList.contains("layout-7"))) {
        if (typeof togglemenulayout === "function") {
            togglemenulayout();
        }
    }
});

function rmactive() {
    var elem = qsa(".pcoded-navbar li.pcoded-hasmenu");
    for (var j = 0; j < elem.length; j++) {
        elem[j].classList.remove("active");
        elem[j].classList.remove("pcoded-trigger");
        if (elem[j].children[1]) {
            elem[j].children[1].removeAttribute("style");
        }
    }
}

function menuhrres() {
    const body = qs("body");
    if (!body || !body.classList.contains("theme-horizontal")) {
        return;
    }

    var vw = window.innerWidth;

    if (vw < 992) {
        setTimeout(function () {
            const shw = qs(".sidenav-horizontal-wrapper");
            const th = qs(".theme-horizontal");

            if (shw) {
                shw.classList.add("sidenav-horizontal-wrapper-dis");
                shw.classList.remove("sidenav-horizontal-wrapper");
            }

            if (th) {
                th.classList.add("theme-horizontal-dis");
                th.classList.remove("theme-horizontal");
            }
        }, 400);
    } else {
        setTimeout(function () {
            const shwd = qs(".sidenav-horizontal-wrapper-dis");
            const thd = qs(".theme-horizontal-dis");

            if (shwd) {
                shwd.classList.add("sidenav-horizontal-wrapper");
                shwd.classList.remove("sidenav-horizontal-wrapper-dis");
            }

            if (thd) {
                thd.classList.add("theme-horizontal");
                thd.classList.remove("theme-horizontal-dis");
            }
        }, 400);
    }

    setTimeout(function () {
        const navbar = qs(".pcoded-navbar");
        const sidenavHorizontal = qs(".sidenav-horizontal-wrapper-dis");

        if (navbar && navbar.classList.contains("theme-horizontal-dis") && sidenavHorizontal) {
            sidenavHorizontal.style.height = "100%";
            sidenavHorizontal.style.position = "relative";

            new PerfectScrollbar(".sidenav-horizontal-wrapper-dis", {
                wheelSpeed: 0.5,
                swipeEasing: 0,
                suppressScrollX: true,
                wheelPropagation: 1,
                minScrollbarLength: 40,
            });
        }
    }, 1000);
}

var ost = 0;

function togglemenu() {
    var vw = window.innerWidth;
    const navbar = qs(".pcoded-navbar");

    if (!navbar) return;

    if (!navbar.classList.contains("theme-horizontal")) {
        const nonHorizontalNavbar = qs(".pcoded-navbar:not(.theme-horizontal)");
        if (!nonHorizontalNavbar) return;

        if (vw <= 1200 && vw >= 992) {
            nonHorizontalNavbar.classList.add("navbar-collapsed");
        }
        if (vw < 992) {
            nonHorizontalNavbar.classList.remove("navbar-collapsed");
        }
    }
}

var tablayclick = qs(".layout1-nav > ul > li");
if (tablayclick) {
    var tc = qsa(".layout1-nav > ul > li");
    for (var t = 0; t < tc.length; t++) {
        var c = tc[t];
        c.addEventListener("click", function (event) {
            var targetElement = event.target;
            if (targetElement.tagName == "A") {
                targetElement = targetElement.parentNode;
            }
            if (targetElement.tagName == "I") {
                targetElement = targetElement.parentNode.parentNode;
            }

            if (!targetElement.children[0]) return;

            var tempcont = targetElement.children[0].getAttribute("data-cont");
            const activeSideLink = qs(".navbar-content .sidelink.active");
            const activeLayout = qs(".layout1-nav > ul > li.active");

            if (activeSideLink) activeSideLink.classList.remove("active");
            if (activeLayout) activeLayout.classList.remove("active");

            targetElement.classList.add("active");

            const newSideLink = qs(".navbar-content .sidelink." + tempcont);
            if (newSideLink) newSideLink.classList.add("active");
        });
    }
}

var tablaymenuclick = qs(".layout-1 .toggle-sidemenu");
if (tablaymenuclick) {
    tablaymenuclick.addEventListener("click", function () {
        const navbar = qs(".pcoded-navbar");
        if (navbar) {
            navbar.classList.toggle("hide-sidemenu");
        }
    });
}

function toggleFullScreen() {
    if (
        !document.fullscreenElement &&
        !document.mozFullScreenElement &&
        !document.webkitFullscreenElement
    ) {
        if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
        } else if (document.documentElement.mozRequestFullScreen) {
            document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullscreen) {
            document.documentElement.webkitRequestFullscreen(Element.ALLOW_KEYBOARD_INPUT);
        }
    } else {
        if (document.cancelFullScreen) {
            document.cancelFullScreen();
        } else if (document.mozCancelFullScreen) {
            document.mozCancelFullScreen();
        } else if (document.webkitCancelFullScreen) {
            document.webkitCancelFullScreen();
        }
    }

    const fullScreenIcon = qs(".full-screen > i");
    if (fullScreenIcon) {
        fullScreenIcon.classList.toggle("icon-maximize");
        fullScreenIcon.classList.toggle("icon-minimize");
    }
}

function menuclick() {
    var elem = qsa(".pcoded-navbar li");
    for (var j = 0; j < elem.length; j++) {
        elem[j].removeEventListener("click", function () {});
    }

    const body = qs("body");
    if (body && body.classList.contains("minimenu")) {
        return;
    }

    var submenus = qsa(".pcoded-navbar li:not(.pcoded-trigger) .pcoded-submenu");
    for (var k = 0; k < submenus.length; k++) {
        submenus[k].style.display = "none";
    }

    var pclinkclick = qsa(".pcoded-inner-navbar > li:not(.pcoded-menu-caption).pcoded-hasmenu");
    for (var i = 0; i < pclinkclick.length; i++) {
        pclinkclick[i].addEventListener("click", function (event) {
            event.stopPropagation();
            var targetElement = event.target;
            if (targetElement.tagName == "SPAN") {
                targetElement = targetElement.parentNode;
            }

            if (!targetElement.parentNode) return;

            if (targetElement.parentNode.classList.contains("pcoded-trigger")) {
                targetElement.parentNode.classList.remove("pcoded-trigger");
                if (targetElement.parentNode.children[1]) {
                    slideUp(targetElement.parentNode.children[1], 200);
                }
            } else {
                var tc = qsa("li.pcoded-trigger.pcoded-hasmenu");
                for (var t = 0; t < tc.length; t++) {
                    var c = tc[t];
                    c.classList.remove("pcoded-trigger");
                    if (c.children[1]) {
                        slideUp(c.children[1], 200);
                    }
                }

                targetElement.parentNode.classList.add("pcoded-trigger");
                if (targetElement.parentNode.children[1]) {
                    slideDown(targetElement.parentNode.children[1], 200);
                }
            }
        });
    }

    var pcsublinkclick = qsa(".pcoded-inner-navbar > li:not(.pcoded-menu-caption) li");
    for (var n = 0; n < pcsublinkclick.length; n++) {
        pcsublinkclick[n].addEventListener("click", function (event) {
            var targetElement = event.target;
            if (targetElement.tagName == "SPAN") {
                targetElement = targetElement.parentNode;
            }

            event.stopPropagation();

            if (!targetElement.parentNode) return;

            if (targetElement.parentNode.classList.contains("pcoded-trigger")) {
                targetElement.parentNode.classList.remove("pcoded-trigger");
                if (targetElement.parentNode.children[1]) {
                    slideUp(targetElement.parentNode.children[1], 200);
                }
            } else {
                var tc = targetElement.parentNode.parentNode ? targetElement.parentNode.parentNode.children : [];
                for (var t = 0; t < tc.length; t++) {
                    var c = tc[t];
                    c.classList.remove("pcoded-trigger");
                    if (c.tagName == "LI" && c.children[0] && c.children[0].parentNode.classList.contains("pcoded-hasmenu")) {
                        slideUp(c.children[0].parentNode.children[1], 200);
                    }
                }

                targetElement.parentNode.classList.add("pcoded-trigger");
                var tmp = targetElement.parentNode.children[1];
                if (tmp) {
                    tmp.removeAttribute("style");
                    slideDown(tmp, 200);
                }
            }
        });
    }
}

if (qs("#mobile-collapse1")) {
    qs("#mobile-collapse1").addEventListener("click", function (e) {
        var vw = window.innerWidth;
        const navbar = qs(".pcoded-navbar");
        if (vw < 992 && navbar) {
            navbar.classList.toggle("mob-open");
            e.stopPropagation();
        }
    });
}

document.addEventListener("DOMContentLoaded", function () {
    var vw = window.innerWidth;
    const navbar = qs(".pcoded-navbar");
    const mainContainer = qs(".pcoded-main-container");

    if (navbar) {
        navbar.addEventListener("click", function (e) {
            e.stopPropagation();
        });
    }

    if (mainContainer) {
        mainContainer.addEventListener("click", function () {
            if (vw < 992 && navbar && navbar.classList.contains("mob-open")) {
                navbar.classList.remove("mob-open");

                const mc = qs("#mobile-collapse");
                const mc1 = qs("#mobile-collapse1");
                if (mc) mc.classList.remove("on");
                if (mc1) mc1.classList.remove("on");
            }
        });
    }
});

var elemLinks = qsa(".pcoded-navbar .pcoded-inner-navbar a");
for (var l = 0; l < elemLinks.length; l++) {
    var pageUrl = window.location.href.split(/[?#]/)[0];
    if (elemLinks[l].href == pageUrl && elemLinks[l].getAttribute("href") != "") {
        elemLinks[l].parentNode.classList.add("active");

        if (
            elemLinks[l].parentNode.parentNode &&
            elemLinks[l].parentNode.parentNode.parentNode
        ) {
            elemLinks[l].parentNode.parentNode.parentNode.classList.add("active");
            elemLinks[l].parentNode.parentNode.parentNode.classList.add("pcoded-trigger");
            elemLinks[l].parentNode.parentNode.style.display = "block";
        }

        if (
            elemLinks[l].parentNode.parentNode.parentNode &&
            elemLinks[l].parentNode.parentNode.parentNode.parentNode &&
            elemLinks[l].parentNode.parentNode.parentNode.parentNode.parentNode
        ) {
            elemLinks[l].parentNode.parentNode.parentNode.parentNode.parentNode.classList.add("active");
            elemLinks[l].parentNode.parentNode.parentNode.parentNode.parentNode.classList.add("pcoded-trigger");
            elemLinks[l].parentNode.parentNode.parentNode.parentNode.style.display = "block";
        }

        if (document.body.classList.contains("tab-layout")) {
            const activeSideLink = qs(".sidelink.active");
            if (activeSideLink) {
                var temp = activeSideLink.getAttribute("data-value");
                const activeLayout = qs(".layout1-nav > ul > li.active");
                if (activeLayout) activeLayout.classList.remove("active");

                const targetTab = qs('.layout1-nav > ul > li > a[data-cont="' + temp + '"]');
                if (targetTab && targetTab.parentNode) {
                    targetTab.parentNode.classList.add("active");
                }
            }
        }
    }
}

let slideUp = (target, duration = 0) => {
    if (!target) return;
    target.style.transitionProperty = "height, margin, padding";
    target.style.transitionDuration = duration + "ms";
    target.style.boxSizing = "border-box";
    target.style.height = target.offsetHeight + "px";
    target.offsetHeight;
    target.style.overflow = "hidden";
    target.style.height = 0;
    target.style.paddingTop = 0;
    target.style.paddingBottom = 0;
    target.style.marginTop = 0;
    target.style.marginBottom = 0;
};

let slideDown = (target, duration = 0) => {
    if (!target) return;
    target.style.removeProperty("display");
    let display = window.getComputedStyle(target).display;

    if (display === "none") display = "block";

    target.style.display = display;
    let height = target.offsetHeight;
    target.style.overflow = "hidden";
    target.style.height = 0;
    target.style.paddingTop = 0;
    target.style.paddingBottom = 0;
    target.style.marginTop = 0;
    target.style.marginBottom = 0;
    target.offsetHeight;
    target.style.boxSizing = "border-box";
    target.style.transitionProperty = "height, margin, padding";
    target.style.transitionDuration = duration + "ms";
    target.style.height = height + "px";
    target.style.removeProperty("padding-top");
    target.style.removeProperty("padding-bottom");
    target.style.removeProperty("margin-top");
    target.style.removeProperty("margin-bottom");

    window.setTimeout(() => {
        target.style.removeProperty("height");
        target.style.removeProperty("overflow");
        target.style.removeProperty("transition-duration");
        target.style.removeProperty("transition-property");
    }, duration);
};

var slideToggle = (target, duration = 0) => {
    if (!target) return;
    if (window.getComputedStyle(target).display === "none") {
        return slideDown(target, duration);
    } else {
        return slideUp(target, duration);
    }
};