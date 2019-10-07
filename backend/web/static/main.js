(window["webpackJsonp"] = window["webpackJsonp"] || []).push([["main"],{

/***/ "./$$_lazy_route_resource lazy recursive":
/*!******************************************************!*\
  !*** ./$$_lazy_route_resource lazy namespace object ***!
  \******************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncaught exception popping up in devtools
	return Promise.resolve().then(function() {
		var e = new Error("Cannot find module '" + req + "'");
		e.code = 'MODULE_NOT_FOUND';
		throw e;
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = "./$$_lazy_route_resource lazy recursive";

/***/ }),

/***/ "./node_modules/@angular-devkit/build-angular/src/angular-cli-files/plugins/raw-css-loader.js!./node_modules/postcss-loader/src/index.js?!./node_modules/leaflet/dist/leaflet.css":
/*!****************************************************************************************************************************************************************************************!*\
  !*** ./node_modules/@angular-devkit/build-angular/src/angular-cli-files/plugins/raw-css-loader.js!./node_modules/postcss-loader/src??embedded!./node_modules/leaflet/dist/leaflet.css ***!
  \****************************************************************************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = [[module.i, "/* required styles */\r\n\r\n.leaflet-pane,\r\n.leaflet-tile,\r\n.leaflet-marker-icon,\r\n.leaflet-marker-shadow,\r\n.leaflet-tile-container,\r\n.leaflet-pane > svg,\r\n.leaflet-pane > canvas,\r\n.leaflet-zoom-box,\r\n.leaflet-image-layer,\r\n.leaflet-layer {\r\n\tposition: absolute;\r\n\tleft: 0;\r\n\ttop: 0;\r\n\t}\r\n\r\n.leaflet-container {\r\n\toverflow: hidden;\r\n\t}\r\n\r\n.leaflet-tile,\r\n.leaflet-marker-icon,\r\n.leaflet-marker-shadow {\r\n\t-webkit-user-select: none;\r\n\t   -moz-user-select: none;\r\n\t        -ms-user-select: none;\r\n\t    user-select: none;\r\n\t  -webkit-user-drag: none;\r\n\t}\r\n\r\n/* Prevents IE11 from highlighting tiles in blue */\r\n\r\n.leaflet-tile::-moz-selection {\r\n\tbackground: transparent;\r\n}\r\n\r\n.leaflet-tile::selection {\r\n\tbackground: transparent;\r\n}\r\n\r\n/* Safari renders non-retina tile on retina better with this, but Chrome is worse */\r\n\r\n.leaflet-safari .leaflet-tile {\r\n\timage-rendering: -webkit-optimize-contrast;\r\n\t}\r\n\r\n/* hack that prevents hw layers \"stretching\" when loading new tiles */\r\n\r\n.leaflet-safari .leaflet-tile-container {\r\n\twidth: 1600px;\r\n\theight: 1600px;\r\n\t-webkit-transform-origin: 0 0;\r\n\t}\r\n\r\n.leaflet-marker-icon,\r\n.leaflet-marker-shadow {\r\n\tdisplay: block;\r\n\t}\r\n\r\n/* .leaflet-container svg: reset svg max-width decleration shipped in Joomla! (joomla.org) 3.x */\r\n\r\n/* .leaflet-container img: map is broken in FF if you have max-width: 100% on tiles */\r\n\r\n.leaflet-container .leaflet-overlay-pane svg,\r\n.leaflet-container .leaflet-marker-pane img,\r\n.leaflet-container .leaflet-shadow-pane img,\r\n.leaflet-container .leaflet-tile-pane img,\r\n.leaflet-container img.leaflet-image-layer,\r\n.leaflet-container .leaflet-tile {\r\n\tmax-width: none !important;\r\n\tmax-height: none !important;\r\n\t}\r\n\r\n.leaflet-container.leaflet-touch-zoom {\r\n\ttouch-action: pan-x pan-y;\r\n\t}\r\n\r\n.leaflet-container.leaflet-touch-drag {\r\n\t/* Fallback for FF which doesn't support pinch-zoom */\r\n\ttouch-action: none;\r\n\ttouch-action: pinch-zoom;\r\n}\r\n\r\n.leaflet-container.leaflet-touch-drag.leaflet-touch-zoom {\r\n\ttouch-action: none;\r\n}\r\n\r\n.leaflet-container {\r\n\t-webkit-tap-highlight-color: transparent;\r\n}\r\n\r\n.leaflet-container a {\r\n\t-webkit-tap-highlight-color: rgba(51, 181, 229, 0.4);\r\n}\r\n\r\n.leaflet-tile {\r\n\t-webkit-filter: inherit;\r\n\t        filter: inherit;\r\n\tvisibility: hidden;\r\n\t}\r\n\r\n.leaflet-tile-loaded {\r\n\tvisibility: inherit;\r\n\t}\r\n\r\n.leaflet-zoom-box {\r\n\twidth: 0;\r\n\theight: 0;\r\n\tbox-sizing: border-box;\r\n\tz-index: 800;\r\n\t}\r\n\r\n/* workaround for https://bugzilla.mozilla.org/show_bug.cgi?id=888319 */\r\n\r\n.leaflet-overlay-pane svg {\r\n\t-moz-user-select: none;\r\n\t}\r\n\r\n.leaflet-pane         { z-index: 400; }\r\n\r\n.leaflet-tile-pane    { z-index: 200; }\r\n\r\n.leaflet-overlay-pane { z-index: 400; }\r\n\r\n.leaflet-shadow-pane  { z-index: 500; }\r\n\r\n.leaflet-marker-pane  { z-index: 600; }\r\n\r\n.leaflet-tooltip-pane   { z-index: 650; }\r\n\r\n.leaflet-popup-pane   { z-index: 700; }\r\n\r\n.leaflet-map-pane canvas { z-index: 100; }\r\n\r\n.leaflet-map-pane svg    { z-index: 200; }\r\n\r\n.leaflet-vml-shape {\r\n\twidth: 1px;\r\n\theight: 1px;\r\n\t}\r\n\r\n.lvml {\r\n\tbehavior: url(#default#VML);\r\n\tdisplay: inline-block;\r\n\tposition: absolute;\r\n\t}\r\n\r\n/* control positioning */\r\n\r\n.leaflet-control {\r\n\tposition: relative;\r\n\tz-index: 800;\r\n\tpointer-events: visiblePainted; /* IE 9-10 doesn't have auto */\r\n\tpointer-events: auto;\r\n\t}\r\n\r\n.leaflet-top,\r\n.leaflet-bottom {\r\n\tposition: absolute;\r\n\tz-index: 1000;\r\n\tpointer-events: none;\r\n\t}\r\n\r\n.leaflet-top {\r\n\ttop: 0;\r\n\t}\r\n\r\n.leaflet-right {\r\n\tright: 0;\r\n\t}\r\n\r\n.leaflet-bottom {\r\n\tbottom: 0;\r\n\t}\r\n\r\n.leaflet-left {\r\n\tleft: 0;\r\n\t}\r\n\r\n.leaflet-control {\r\n\tfloat: left;\r\n\tclear: both;\r\n\t}\r\n\r\n.leaflet-right .leaflet-control {\r\n\tfloat: right;\r\n\t}\r\n\r\n.leaflet-top .leaflet-control {\r\n\tmargin-top: 10px;\r\n\t}\r\n\r\n.leaflet-bottom .leaflet-control {\r\n\tmargin-bottom: 10px;\r\n\t}\r\n\r\n.leaflet-left .leaflet-control {\r\n\tmargin-left: 10px;\r\n\t}\r\n\r\n.leaflet-right .leaflet-control {\r\n\tmargin-right: 10px;\r\n\t}\r\n\r\n/* zoom and fade animations */\r\n\r\n.leaflet-fade-anim .leaflet-tile {\r\n\twill-change: opacity;\r\n\t}\r\n\r\n.leaflet-fade-anim .leaflet-popup {\r\n\topacity: 0;\r\n\ttransition: opacity 0.2s linear;\r\n\t}\r\n\r\n.leaflet-fade-anim .leaflet-map-pane .leaflet-popup {\r\n\topacity: 1;\r\n\t}\r\n\r\n.leaflet-zoom-animated {\r\n\t-webkit-transform-origin: 0 0;\r\n\t        transform-origin: 0 0;\r\n\t}\r\n\r\n.leaflet-zoom-anim .leaflet-zoom-animated {\r\n\twill-change: transform;\r\n\t}\r\n\r\n.leaflet-zoom-anim .leaflet-zoom-animated {\r\n\ttransition:         -webkit-transform 0.25s cubic-bezier(0,0,0.25,1);\r\n\ttransition:         transform 0.25s cubic-bezier(0,0,0.25,1);\r\n\ttransition:         transform 0.25s cubic-bezier(0,0,0.25,1), -webkit-transform 0.25s cubic-bezier(0,0,0.25,1);\r\n\t}\r\n\r\n.leaflet-zoom-anim .leaflet-tile,\r\n.leaflet-pan-anim .leaflet-tile {\r\n\ttransition: none;\r\n\t}\r\n\r\n.leaflet-zoom-anim .leaflet-zoom-hide {\r\n\tvisibility: hidden;\r\n\t}\r\n\r\n/* cursors */\r\n\r\n.leaflet-interactive {\r\n\tcursor: pointer;\r\n\t}\r\n\r\n.leaflet-grab {\r\n\tcursor: -webkit-grab;\r\n\tcursor:         grab;\r\n\t}\r\n\r\n.leaflet-crosshair,\r\n.leaflet-crosshair .leaflet-interactive {\r\n\tcursor: crosshair;\r\n\t}\r\n\r\n.leaflet-popup-pane,\r\n.leaflet-control {\r\n\tcursor: auto;\r\n\t}\r\n\r\n.leaflet-dragging .leaflet-grab,\r\n.leaflet-dragging .leaflet-grab .leaflet-interactive,\r\n.leaflet-dragging .leaflet-marker-draggable {\r\n\tcursor: move;\r\n\tcursor: -webkit-grabbing;\r\n\tcursor:         grabbing;\r\n\t}\r\n\r\n/* marker & overlays interactivity */\r\n\r\n.leaflet-marker-icon,\r\n.leaflet-marker-shadow,\r\n.leaflet-image-layer,\r\n.leaflet-pane > svg path,\r\n.leaflet-tile-container {\r\n\tpointer-events: none;\r\n\t}\r\n\r\n.leaflet-marker-icon.leaflet-interactive,\r\n.leaflet-image-layer.leaflet-interactive,\r\n.leaflet-pane > svg path.leaflet-interactive,\r\nsvg.leaflet-image-layer.leaflet-interactive path {\r\n\tpointer-events: visiblePainted; /* IE 9-10 doesn't have auto */\r\n\tpointer-events: auto;\r\n\t}\r\n\r\n/* visual tweaks */\r\n\r\n.leaflet-container {\r\n\tbackground: #ddd;\r\n\toutline: 0;\r\n\t}\r\n\r\n.leaflet-container a {\r\n\tcolor: #0078A8;\r\n\t}\r\n\r\n.leaflet-container a.leaflet-active {\r\n\toutline: 2px solid orange;\r\n\t}\r\n\r\n.leaflet-zoom-box {\r\n\tborder: 2px dotted #38f;\r\n\tbackground: rgba(255,255,255,0.5);\r\n\t}\r\n\r\n/* general typography */\r\n\r\n.leaflet-container {\r\n\tfont: 12px/1.5 \"Helvetica Neue\", Arial, Helvetica, sans-serif;\r\n\t}\r\n\r\n/* general toolbar styles */\r\n\r\n.leaflet-bar {\r\n\tbox-shadow: 0 1px 5px rgba(0,0,0,0.65);\r\n\tborder-radius: 4px;\r\n\t}\r\n\r\n.leaflet-bar a,\r\n.leaflet-bar a:hover {\r\n\tbackground-color: #fff;\r\n\tborder-bottom: 1px solid #ccc;\r\n\twidth: 26px;\r\n\theight: 26px;\r\n\tline-height: 26px;\r\n\tdisplay: block;\r\n\ttext-align: center;\r\n\ttext-decoration: none;\r\n\tcolor: black;\r\n\t}\r\n\r\n.leaflet-bar a,\r\n.leaflet-control-layers-toggle {\r\n\tbackground-position: 50% 50%;\r\n\tbackground-repeat: no-repeat;\r\n\tdisplay: block;\r\n\t}\r\n\r\n.leaflet-bar a:hover {\r\n\tbackground-color: #f4f4f4;\r\n\t}\r\n\r\n.leaflet-bar a:first-child {\r\n\tborder-top-left-radius: 4px;\r\n\tborder-top-right-radius: 4px;\r\n\t}\r\n\r\n.leaflet-bar a:last-child {\r\n\tborder-bottom-left-radius: 4px;\r\n\tborder-bottom-right-radius: 4px;\r\n\tborder-bottom: none;\r\n\t}\r\n\r\n.leaflet-bar a.leaflet-disabled {\r\n\tcursor: default;\r\n\tbackground-color: #f4f4f4;\r\n\tcolor: #bbb;\r\n\t}\r\n\r\n.leaflet-touch .leaflet-bar a {\r\n\twidth: 30px;\r\n\theight: 30px;\r\n\tline-height: 30px;\r\n\t}\r\n\r\n.leaflet-touch .leaflet-bar a:first-child {\r\n\tborder-top-left-radius: 2px;\r\n\tborder-top-right-radius: 2px;\r\n\t}\r\n\r\n.leaflet-touch .leaflet-bar a:last-child {\r\n\tborder-bottom-left-radius: 2px;\r\n\tborder-bottom-right-radius: 2px;\r\n\t}\r\n\r\n/* zoom control */\r\n\r\n.leaflet-control-zoom-in,\r\n.leaflet-control-zoom-out {\r\n\tfont: bold 18px 'Lucida Console', Monaco, monospace;\r\n\ttext-indent: 1px;\r\n\t}\r\n\r\n.leaflet-touch .leaflet-control-zoom-in, .leaflet-touch .leaflet-control-zoom-out  {\r\n\tfont-size: 22px;\r\n\t}\r\n\r\n/* layers control */\r\n\r\n.leaflet-control-layers {\r\n\tbox-shadow: 0 1px 5px rgba(0,0,0,0.4);\r\n\tbackground: #fff;\r\n\tborder-radius: 5px;\r\n\t}\r\n\r\n.leaflet-control-layers-toggle {\r\n\tbackground-image: url('layers.png');\r\n\twidth: 36px;\r\n\theight: 36px;\r\n\t}\r\n\r\n.leaflet-retina .leaflet-control-layers-toggle {\r\n\tbackground-image: url('layers-2x.png');\r\n\tbackground-size: 26px 26px;\r\n\t}\r\n\r\n.leaflet-touch .leaflet-control-layers-toggle {\r\n\twidth: 44px;\r\n\theight: 44px;\r\n\t}\r\n\r\n.leaflet-control-layers .leaflet-control-layers-list,\r\n.leaflet-control-layers-expanded .leaflet-control-layers-toggle {\r\n\tdisplay: none;\r\n\t}\r\n\r\n.leaflet-control-layers-expanded .leaflet-control-layers-list {\r\n\tdisplay: block;\r\n\tposition: relative;\r\n\t}\r\n\r\n.leaflet-control-layers-expanded {\r\n\tpadding: 6px 10px 6px 6px;\r\n\tcolor: #333;\r\n\tbackground: #fff;\r\n\t}\r\n\r\n.leaflet-control-layers-scrollbar {\r\n\toverflow-y: scroll;\r\n\toverflow-x: hidden;\r\n\tpadding-right: 5px;\r\n\t}\r\n\r\n.leaflet-control-layers-selector {\r\n\tmargin-top: 2px;\r\n\tposition: relative;\r\n\ttop: 1px;\r\n\t}\r\n\r\n.leaflet-control-layers label {\r\n\tdisplay: block;\r\n\t}\r\n\r\n.leaflet-control-layers-separator {\r\n\theight: 0;\r\n\tborder-top: 1px solid #ddd;\r\n\tmargin: 5px -10px 5px -6px;\r\n\t}\r\n\r\n/* Default icon URLs */\r\n\r\n.leaflet-default-icon-path {\r\n\tbackground-image: url('marker-icon.png');\r\n\t}\r\n\r\n/* attribution and scale controls */\r\n\r\n.leaflet-container .leaflet-control-attribution {\r\n\tbackground: #fff;\r\n\tbackground: rgba(255, 255, 255, 0.7);\r\n\tmargin: 0;\r\n\t}\r\n\r\n.leaflet-control-attribution,\r\n.leaflet-control-scale-line {\r\n\tpadding: 0 5px;\r\n\tcolor: #333;\r\n\t}\r\n\r\n.leaflet-control-attribution a {\r\n\ttext-decoration: none;\r\n\t}\r\n\r\n.leaflet-control-attribution a:hover {\r\n\ttext-decoration: underline;\r\n\t}\r\n\r\n.leaflet-container .leaflet-control-attribution,\r\n.leaflet-container .leaflet-control-scale {\r\n\tfont-size: 11px;\r\n\t}\r\n\r\n.leaflet-left .leaflet-control-scale {\r\n\tmargin-left: 5px;\r\n\t}\r\n\r\n.leaflet-bottom .leaflet-control-scale {\r\n\tmargin-bottom: 5px;\r\n\t}\r\n\r\n.leaflet-control-scale-line {\r\n\tborder: 2px solid #777;\r\n\tborder-top: none;\r\n\tline-height: 1.1;\r\n\tpadding: 2px 5px 1px;\r\n\tfont-size: 11px;\r\n\twhite-space: nowrap;\r\n\toverflow: hidden;\r\n\tbox-sizing: border-box;\r\n\r\n\tbackground: #fff;\r\n\tbackground: rgba(255, 255, 255, 0.5);\r\n\t}\r\n\r\n.leaflet-control-scale-line:not(:first-child) {\r\n\tborder-top: 2px solid #777;\r\n\tborder-bottom: none;\r\n\tmargin-top: -2px;\r\n\t}\r\n\r\n.leaflet-control-scale-line:not(:first-child):not(:last-child) {\r\n\tborder-bottom: 2px solid #777;\r\n\t}\r\n\r\n.leaflet-touch .leaflet-control-attribution,\r\n.leaflet-touch .leaflet-control-layers,\r\n.leaflet-touch .leaflet-bar {\r\n\tbox-shadow: none;\r\n\t}\r\n\r\n.leaflet-touch .leaflet-control-layers,\r\n.leaflet-touch .leaflet-bar {\r\n\tborder: 2px solid rgba(0,0,0,0.2);\r\n\tbackground-clip: padding-box;\r\n\t}\r\n\r\n/* popup */\r\n\r\n.leaflet-popup {\r\n\tposition: absolute;\r\n\ttext-align: center;\r\n\tmargin-bottom: 20px;\r\n\t}\r\n\r\n.leaflet-popup-content-wrapper {\r\n\tpadding: 1px;\r\n\ttext-align: left;\r\n\tborder-radius: 12px;\r\n\t}\r\n\r\n.leaflet-popup-content {\r\n\tmargin: 13px 19px;\r\n\tline-height: 1.4;\r\n\t}\r\n\r\n.leaflet-popup-content p {\r\n\tmargin: 18px 0;\r\n\t}\r\n\r\n.leaflet-popup-tip-container {\r\n\twidth: 40px;\r\n\theight: 20px;\r\n\tposition: absolute;\r\n\tleft: 50%;\r\n\tmargin-left: -20px;\r\n\toverflow: hidden;\r\n\tpointer-events: none;\r\n\t}\r\n\r\n.leaflet-popup-tip {\r\n\twidth: 17px;\r\n\theight: 17px;\r\n\tpadding: 1px;\r\n\r\n\tmargin: -10px auto 0;\r\n\r\n\t-webkit-transform: rotate(45deg);\r\n\t        transform: rotate(45deg);\r\n\t}\r\n\r\n.leaflet-popup-content-wrapper,\r\n.leaflet-popup-tip {\r\n\tbackground: white;\r\n\tcolor: #333;\r\n\tbox-shadow: 0 3px 14px rgba(0,0,0,0.4);\r\n\t}\r\n\r\n.leaflet-container a.leaflet-popup-close-button {\r\n\tposition: absolute;\r\n\ttop: 0;\r\n\tright: 0;\r\n\tpadding: 4px 4px 0 0;\r\n\tborder: none;\r\n\ttext-align: center;\r\n\twidth: 18px;\r\n\theight: 14px;\r\n\tfont: 16px/14px Tahoma, Verdana, sans-serif;\r\n\tcolor: #c3c3c3;\r\n\ttext-decoration: none;\r\n\tfont-weight: bold;\r\n\tbackground: transparent;\r\n\t}\r\n\r\n.leaflet-container a.leaflet-popup-close-button:hover {\r\n\tcolor: #999;\r\n\t}\r\n\r\n.leaflet-popup-scrolled {\r\n\toverflow: auto;\r\n\tborder-bottom: 1px solid #ddd;\r\n\tborder-top: 1px solid #ddd;\r\n\t}\r\n\r\n.leaflet-oldie .leaflet-popup-content-wrapper {\r\n\tzoom: 1;\r\n\t}\r\n\r\n.leaflet-oldie .leaflet-popup-tip {\r\n\twidth: 24px;\r\n\tmargin: 0 auto;\r\n\r\n\t-ms-filter: \"progid:DXImageTransform.Microsoft.Matrix(M11=0.70710678, M12=0.70710678, M21=-0.70710678, M22=0.70710678)\";\r\n\tfilter: progid:DXImageTransform.Microsoft.Matrix(M11=0.70710678, M12=0.70710678, M21=-0.70710678, M22=0.70710678);\r\n\t}\r\n\r\n.leaflet-oldie .leaflet-popup-tip-container {\r\n\tmargin-top: -1px;\r\n\t}\r\n\r\n.leaflet-oldie .leaflet-control-zoom,\r\n.leaflet-oldie .leaflet-control-layers,\r\n.leaflet-oldie .leaflet-popup-content-wrapper,\r\n.leaflet-oldie .leaflet-popup-tip {\r\n\tborder: 1px solid #999;\r\n\t}\r\n\r\n/* div icon */\r\n\r\n.leaflet-div-icon {\r\n\tbackground: #fff;\r\n\tborder: 1px solid #666;\r\n\t}\r\n\r\n/* Tooltip */\r\n\r\n/* Base styles for the element that has a tooltip */\r\n\r\n.leaflet-tooltip {\r\n\tposition: absolute;\r\n\tpadding: 6px;\r\n\tbackground-color: #fff;\r\n\tborder: 1px solid #fff;\r\n\tborder-radius: 3px;\r\n\tcolor: #222;\r\n\twhite-space: nowrap;\r\n\t-webkit-user-select: none;\r\n\t-moz-user-select: none;\r\n\t-ms-user-select: none;\r\n\tuser-select: none;\r\n\tpointer-events: none;\r\n\tbox-shadow: 0 1px 3px rgba(0,0,0,0.4);\r\n\t}\r\n\r\n.leaflet-tooltip.leaflet-clickable {\r\n\tcursor: pointer;\r\n\tpointer-events: auto;\r\n\t}\r\n\r\n.leaflet-tooltip-top:before,\r\n.leaflet-tooltip-bottom:before,\r\n.leaflet-tooltip-left:before,\r\n.leaflet-tooltip-right:before {\r\n\tposition: absolute;\r\n\tpointer-events: none;\r\n\tborder: 6px solid transparent;\r\n\tbackground: transparent;\r\n\tcontent: \"\";\r\n\t}\r\n\r\n/* Directions */\r\n\r\n.leaflet-tooltip-bottom {\r\n\tmargin-top: 6px;\r\n}\r\n\r\n.leaflet-tooltip-top {\r\n\tmargin-top: -6px;\r\n}\r\n\r\n.leaflet-tooltip-bottom:before,\r\n.leaflet-tooltip-top:before {\r\n\tleft: 50%;\r\n\tmargin-left: -6px;\r\n\t}\r\n\r\n.leaflet-tooltip-top:before {\r\n\tbottom: 0;\r\n\tmargin-bottom: -12px;\r\n\tborder-top-color: #fff;\r\n\t}\r\n\r\n.leaflet-tooltip-bottom:before {\r\n\ttop: 0;\r\n\tmargin-top: -12px;\r\n\tmargin-left: -6px;\r\n\tborder-bottom-color: #fff;\r\n\t}\r\n\r\n.leaflet-tooltip-left {\r\n\tmargin-left: -6px;\r\n}\r\n\r\n.leaflet-tooltip-right {\r\n\tmargin-left: 6px;\r\n}\r\n\r\n.leaflet-tooltip-left:before,\r\n.leaflet-tooltip-right:before {\r\n\ttop: 50%;\r\n\tmargin-top: -6px;\r\n\t}\r\n\r\n.leaflet-tooltip-left:before {\r\n\tright: 0;\r\n\tmargin-right: -12px;\r\n\tborder-left-color: #fff;\r\n\t}\r\n\r\n.leaflet-tooltip-right:before {\r\n\tleft: 0;\r\n\tmargin-left: -12px;\r\n\tborder-right-color: #fff;\r\n\t}\r\n\r\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIm5vZGVfbW9kdWxlcy9sZWFmbGV0L2Rpc3QvbGVhZmxldC5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUEsb0JBQW9COztBQUVwQjs7Ozs7Ozs7OztDQVVDLGtCQUFrQjtDQUNsQixPQUFPO0NBQ1AsTUFBTTtDQUNOOztBQUNEO0NBQ0MsZ0JBQWdCO0NBQ2hCOztBQUNEOzs7Q0FHQyx5QkFBeUI7SUFDdEIsc0JBQXNCO1NBQ2pCLHFCQUFpQjtLQUFqQixpQkFBaUI7R0FDdkIsdUJBQXVCO0NBQ3pCOztBQUNELGtEQUFrRDs7QUFDbEQ7Q0FDQyx1QkFBdUI7QUFDeEI7O0FBRkE7Q0FDQyx1QkFBdUI7QUFDeEI7O0FBQ0EsbUZBQW1GOztBQUNuRjtDQUNDLDBDQUEwQztDQUMxQzs7QUFDRCxxRUFBcUU7O0FBQ3JFO0NBQ0MsYUFBYTtDQUNiLGNBQWM7Q0FDZCw2QkFBNkI7Q0FDN0I7O0FBQ0Q7O0NBRUMsY0FBYztDQUNkOztBQUNELGdHQUFnRzs7QUFDaEcscUZBQXFGOztBQUNyRjs7Ozs7O0NBTUMsMEJBQTBCO0NBQzFCLDJCQUEyQjtDQUMzQjs7QUFFRDtDQUVDLHlCQUF5QjtDQUN6Qjs7QUFDRDtDQUVDLHFEQUFxRDtDQUNyRCxrQkFBa0I7Q0FDbEIsd0JBQXdCO0FBQ3pCOztBQUNBO0NBRUMsa0JBQWtCO0FBQ25COztBQUNBO0NBQ0Msd0NBQXdDO0FBQ3pDOztBQUNBO0NBQ0Msb0RBQW9EO0FBQ3JEOztBQUNBO0NBQ0MsdUJBQWU7U0FBZixlQUFlO0NBQ2Ysa0JBQWtCO0NBQ2xCOztBQUNEO0NBQ0MsbUJBQW1CO0NBQ25COztBQUNEO0NBQ0MsUUFBUTtDQUNSLFNBQVM7Q0FFSixzQkFBc0I7Q0FDM0IsWUFBWTtDQUNaOztBQUNELHVFQUF1RTs7QUFDdkU7Q0FDQyxzQkFBc0I7Q0FDdEI7O0FBRUQsd0JBQXdCLFlBQVksRUFBRTs7QUFFdEMsd0JBQXdCLFlBQVksRUFBRTs7QUFDdEMsd0JBQXdCLFlBQVksRUFBRTs7QUFDdEMsd0JBQXdCLFlBQVksRUFBRTs7QUFDdEMsd0JBQXdCLFlBQVksRUFBRTs7QUFDdEMsMEJBQTBCLFlBQVksRUFBRTs7QUFDeEMsd0JBQXdCLFlBQVksRUFBRTs7QUFFdEMsMkJBQTJCLFlBQVksRUFBRTs7QUFDekMsMkJBQTJCLFlBQVksRUFBRTs7QUFFekM7Q0FDQyxVQUFVO0NBQ1YsV0FBVztDQUNYOztBQUNEO0NBQ0MsMkJBQTJCO0NBQzNCLHFCQUFxQjtDQUNyQixrQkFBa0I7Q0FDbEI7O0FBR0Qsd0JBQXdCOztBQUV4QjtDQUNDLGtCQUFrQjtDQUNsQixZQUFZO0NBQ1osOEJBQThCLEVBQUUsOEJBQThCO0NBQzlELG9CQUFvQjtDQUNwQjs7QUFDRDs7Q0FFQyxrQkFBa0I7Q0FDbEIsYUFBYTtDQUNiLG9CQUFvQjtDQUNwQjs7QUFDRDtDQUNDLE1BQU07Q0FDTjs7QUFDRDtDQUNDLFFBQVE7Q0FDUjs7QUFDRDtDQUNDLFNBQVM7Q0FDVDs7QUFDRDtDQUNDLE9BQU87Q0FDUDs7QUFDRDtDQUNDLFdBQVc7Q0FDWCxXQUFXO0NBQ1g7O0FBQ0Q7Q0FDQyxZQUFZO0NBQ1o7O0FBQ0Q7Q0FDQyxnQkFBZ0I7Q0FDaEI7O0FBQ0Q7Q0FDQyxtQkFBbUI7Q0FDbkI7O0FBQ0Q7Q0FDQyxpQkFBaUI7Q0FDakI7O0FBQ0Q7Q0FDQyxrQkFBa0I7Q0FDbEI7O0FBR0QsNkJBQTZCOztBQUU3QjtDQUNDLG9CQUFvQjtDQUNwQjs7QUFDRDtDQUNDLFVBQVU7Q0FHRiwrQkFBK0I7Q0FDdkM7O0FBQ0Q7Q0FDQyxVQUFVO0NBQ1Y7O0FBQ0Q7Q0FDQyw2QkFBNkI7U0FFckIscUJBQXFCO0NBQzdCOztBQUNEO0NBQ0Msc0JBQXNCO0NBQ3RCOztBQUNEO0NBR1Msb0VBQTREO0NBQTVELDREQUE0RDtDQUE1RCw4R0FBNEQ7Q0FDcEU7O0FBQ0Q7O0NBSVMsZ0JBQWdCO0NBQ3hCOztBQUVEO0NBQ0Msa0JBQWtCO0NBQ2xCOztBQUdELFlBQVk7O0FBRVo7Q0FDQyxlQUFlO0NBQ2Y7O0FBQ0Q7Q0FDQyxvQkFBb0I7Q0FFcEIsb0JBQW9CO0NBQ3BCOztBQUNEOztDQUVDLGlCQUFpQjtDQUNqQjs7QUFDRDs7Q0FFQyxZQUFZO0NBQ1o7O0FBQ0Q7OztDQUdDLFlBQVk7Q0FDWix3QkFBd0I7Q0FFeEIsd0JBQXdCO0NBQ3hCOztBQUVELG9DQUFvQzs7QUFDcEM7Ozs7O0NBS0Msb0JBQW9CO0NBQ3BCOztBQUVEOzs7O0NBSUMsOEJBQThCLEVBQUUsOEJBQThCO0NBQzlELG9CQUFvQjtDQUNwQjs7QUFFRCxrQkFBa0I7O0FBRWxCO0NBQ0MsZ0JBQWdCO0NBQ2hCLFVBQVU7Q0FDVjs7QUFDRDtDQUNDLGNBQWM7Q0FDZDs7QUFDRDtDQUNDLHlCQUF5QjtDQUN6Qjs7QUFDRDtDQUNDLHVCQUF1QjtDQUN2QixpQ0FBaUM7Q0FDakM7O0FBR0QsdUJBQXVCOztBQUN2QjtDQUNDLDZEQUE2RDtDQUM3RDs7QUFHRCwyQkFBMkI7O0FBRTNCO0NBQ0Msc0NBQXNDO0NBQ3RDLGtCQUFrQjtDQUNsQjs7QUFDRDs7Q0FFQyxzQkFBc0I7Q0FDdEIsNkJBQTZCO0NBQzdCLFdBQVc7Q0FDWCxZQUFZO0NBQ1osaUJBQWlCO0NBQ2pCLGNBQWM7Q0FDZCxrQkFBa0I7Q0FDbEIscUJBQXFCO0NBQ3JCLFlBQVk7Q0FDWjs7QUFDRDs7Q0FFQyw0QkFBNEI7Q0FDNUIsNEJBQTRCO0NBQzVCLGNBQWM7Q0FDZDs7QUFDRDtDQUNDLHlCQUF5QjtDQUN6Qjs7QUFDRDtDQUNDLDJCQUEyQjtDQUMzQiw0QkFBNEI7Q0FDNUI7O0FBQ0Q7Q0FDQyw4QkFBOEI7Q0FDOUIsK0JBQStCO0NBQy9CLG1CQUFtQjtDQUNuQjs7QUFDRDtDQUNDLGVBQWU7Q0FDZix5QkFBeUI7Q0FDekIsV0FBVztDQUNYOztBQUVEO0NBQ0MsV0FBVztDQUNYLFlBQVk7Q0FDWixpQkFBaUI7Q0FDakI7O0FBQ0Q7Q0FDQywyQkFBMkI7Q0FDM0IsNEJBQTRCO0NBQzVCOztBQUNEO0NBQ0MsOEJBQThCO0NBQzlCLCtCQUErQjtDQUMvQjs7QUFFRCxpQkFBaUI7O0FBRWpCOztDQUVDLG1EQUFtRDtDQUNuRCxnQkFBZ0I7Q0FDaEI7O0FBRUQ7Q0FDQyxlQUFlO0NBQ2Y7O0FBR0QsbUJBQW1COztBQUVuQjtDQUNDLHFDQUFxQztDQUNyQyxnQkFBZ0I7Q0FDaEIsa0JBQWtCO0NBQ2xCOztBQUNEO0NBQ0MsbUNBQXdDO0NBQ3hDLFdBQVc7Q0FDWCxZQUFZO0NBQ1o7O0FBQ0Q7Q0FDQyxzQ0FBMkM7Q0FDM0MsMEJBQTBCO0NBQzFCOztBQUNEO0NBQ0MsV0FBVztDQUNYLFlBQVk7Q0FDWjs7QUFDRDs7Q0FFQyxhQUFhO0NBQ2I7O0FBQ0Q7Q0FDQyxjQUFjO0NBQ2Qsa0JBQWtCO0NBQ2xCOztBQUNEO0NBQ0MseUJBQXlCO0NBQ3pCLFdBQVc7Q0FDWCxnQkFBZ0I7Q0FDaEI7O0FBQ0Q7Q0FDQyxrQkFBa0I7Q0FDbEIsa0JBQWtCO0NBQ2xCLGtCQUFrQjtDQUNsQjs7QUFDRDtDQUNDLGVBQWU7Q0FDZixrQkFBa0I7Q0FDbEIsUUFBUTtDQUNSOztBQUNEO0NBQ0MsY0FBYztDQUNkOztBQUNEO0NBQ0MsU0FBUztDQUNULDBCQUEwQjtDQUMxQiwwQkFBMEI7Q0FDMUI7O0FBRUQsc0JBQXNCOztBQUN0QjtDQUNDLHdDQUE2QztDQUM3Qzs7QUFHRCxtQ0FBbUM7O0FBRW5DO0NBQ0MsZ0JBQWdCO0NBQ2hCLG9DQUFvQztDQUNwQyxTQUFTO0NBQ1Q7O0FBQ0Q7O0NBRUMsY0FBYztDQUNkLFdBQVc7Q0FDWDs7QUFDRDtDQUNDLHFCQUFxQjtDQUNyQjs7QUFDRDtDQUNDLDBCQUEwQjtDQUMxQjs7QUFDRDs7Q0FFQyxlQUFlO0NBQ2Y7O0FBQ0Q7Q0FDQyxnQkFBZ0I7Q0FDaEI7O0FBQ0Q7Q0FDQyxrQkFBa0I7Q0FDbEI7O0FBQ0Q7Q0FDQyxzQkFBc0I7Q0FDdEIsZ0JBQWdCO0NBQ2hCLGdCQUFnQjtDQUNoQixvQkFBb0I7Q0FDcEIsZUFBZTtDQUNmLG1CQUFtQjtDQUNuQixnQkFBZ0I7Q0FFWCxzQkFBc0I7O0NBRTNCLGdCQUFnQjtDQUNoQixvQ0FBb0M7Q0FDcEM7O0FBQ0Q7Q0FDQywwQkFBMEI7Q0FDMUIsbUJBQW1CO0NBQ25CLGdCQUFnQjtDQUNoQjs7QUFDRDtDQUNDLDZCQUE2QjtDQUM3Qjs7QUFFRDs7O0NBR0MsZ0JBQWdCO0NBQ2hCOztBQUNEOztDQUVDLGlDQUFpQztDQUNqQyw0QkFBNEI7Q0FDNUI7O0FBR0QsVUFBVTs7QUFFVjtDQUNDLGtCQUFrQjtDQUNsQixrQkFBa0I7Q0FDbEIsbUJBQW1CO0NBQ25COztBQUNEO0NBQ0MsWUFBWTtDQUNaLGdCQUFnQjtDQUNoQixtQkFBbUI7Q0FDbkI7O0FBQ0Q7Q0FDQyxpQkFBaUI7Q0FDakIsZ0JBQWdCO0NBQ2hCOztBQUNEO0NBQ0MsY0FBYztDQUNkOztBQUNEO0NBQ0MsV0FBVztDQUNYLFlBQVk7Q0FDWixrQkFBa0I7Q0FDbEIsU0FBUztDQUNULGtCQUFrQjtDQUNsQixnQkFBZ0I7Q0FDaEIsb0JBQW9CO0NBQ3BCOztBQUNEO0NBQ0MsV0FBVztDQUNYLFlBQVk7Q0FDWixZQUFZOztDQUVaLG9CQUFvQjs7Q0FFcEIsZ0NBQWdDO1NBR3hCLHdCQUF3QjtDQUNoQzs7QUFDRDs7Q0FFQyxpQkFBaUI7Q0FDakIsV0FBVztDQUNYLHNDQUFzQztDQUN0Qzs7QUFDRDtDQUNDLGtCQUFrQjtDQUNsQixNQUFNO0NBQ04sUUFBUTtDQUNSLG9CQUFvQjtDQUNwQixZQUFZO0NBQ1osa0JBQWtCO0NBQ2xCLFdBQVc7Q0FDWCxZQUFZO0NBQ1osMkNBQTJDO0NBQzNDLGNBQWM7Q0FDZCxxQkFBcUI7Q0FDckIsaUJBQWlCO0NBQ2pCLHVCQUF1QjtDQUN2Qjs7QUFDRDtDQUNDLFdBQVc7Q0FDWDs7QUFDRDtDQUNDLGNBQWM7Q0FDZCw2QkFBNkI7Q0FDN0IsMEJBQTBCO0NBQzFCOztBQUVEO0NBQ0MsT0FBTztDQUNQOztBQUNEO0NBQ0MsV0FBVztDQUNYLGNBQWM7O0NBRWQsdUhBQXVIO0NBQ3ZILGlIQUFpSDtDQUNqSDs7QUFDRDtDQUNDLGdCQUFnQjtDQUNoQjs7QUFFRDs7OztDQUlDLHNCQUFzQjtDQUN0Qjs7QUFHRCxhQUFhOztBQUViO0NBQ0MsZ0JBQWdCO0NBQ2hCLHNCQUFzQjtDQUN0Qjs7QUFHRCxZQUFZOztBQUNaLG1EQUFtRDs7QUFDbkQ7Q0FDQyxrQkFBa0I7Q0FDbEIsWUFBWTtDQUNaLHNCQUFzQjtDQUN0QixzQkFBc0I7Q0FDdEIsa0JBQWtCO0NBQ2xCLFdBQVc7Q0FDWCxtQkFBbUI7Q0FDbkIseUJBQXlCO0NBQ3pCLHNCQUFzQjtDQUN0QixxQkFBcUI7Q0FDckIsaUJBQWlCO0NBQ2pCLG9CQUFvQjtDQUNwQixxQ0FBcUM7Q0FDckM7O0FBQ0Q7Q0FDQyxlQUFlO0NBQ2Ysb0JBQW9CO0NBQ3BCOztBQUNEOzs7O0NBSUMsa0JBQWtCO0NBQ2xCLG9CQUFvQjtDQUNwQiw2QkFBNkI7Q0FDN0IsdUJBQXVCO0NBQ3ZCLFdBQVc7Q0FDWDs7QUFFRCxlQUFlOztBQUVmO0NBQ0MsZUFBZTtBQUNoQjs7QUFDQTtDQUNDLGdCQUFnQjtBQUNqQjs7QUFDQTs7Q0FFQyxTQUFTO0NBQ1QsaUJBQWlCO0NBQ2pCOztBQUNEO0NBQ0MsU0FBUztDQUNULG9CQUFvQjtDQUNwQixzQkFBc0I7Q0FDdEI7O0FBQ0Q7Q0FDQyxNQUFNO0NBQ04saUJBQWlCO0NBQ2pCLGlCQUFpQjtDQUNqQix5QkFBeUI7Q0FDekI7O0FBQ0Q7Q0FDQyxpQkFBaUI7QUFDbEI7O0FBQ0E7Q0FDQyxnQkFBZ0I7QUFDakI7O0FBQ0E7O0NBRUMsUUFBUTtDQUNSLGdCQUFnQjtDQUNoQjs7QUFDRDtDQUNDLFFBQVE7Q0FDUixtQkFBbUI7Q0FDbkIsdUJBQXVCO0NBQ3ZCOztBQUNEO0NBQ0MsT0FBTztDQUNQLGtCQUFrQjtDQUNsQix3QkFBd0I7Q0FDeEIiLCJmaWxlIjoibm9kZV9tb2R1bGVzL2xlYWZsZXQvZGlzdC9sZWFmbGV0LmNzcyIsInNvdXJjZXNDb250ZW50IjpbIi8qIHJlcXVpcmVkIHN0eWxlcyAqL1xyXG5cclxuLmxlYWZsZXQtcGFuZSxcclxuLmxlYWZsZXQtdGlsZSxcclxuLmxlYWZsZXQtbWFya2VyLWljb24sXHJcbi5sZWFmbGV0LW1hcmtlci1zaGFkb3csXHJcbi5sZWFmbGV0LXRpbGUtY29udGFpbmVyLFxyXG4ubGVhZmxldC1wYW5lID4gc3ZnLFxyXG4ubGVhZmxldC1wYW5lID4gY2FudmFzLFxyXG4ubGVhZmxldC16b29tLWJveCxcclxuLmxlYWZsZXQtaW1hZ2UtbGF5ZXIsXHJcbi5sZWFmbGV0LWxheWVyIHtcclxuXHRwb3NpdGlvbjogYWJzb2x1dGU7XHJcblx0bGVmdDogMDtcclxuXHR0b3A6IDA7XHJcblx0fVxyXG4ubGVhZmxldC1jb250YWluZXIge1xyXG5cdG92ZXJmbG93OiBoaWRkZW47XHJcblx0fVxyXG4ubGVhZmxldC10aWxlLFxyXG4ubGVhZmxldC1tYXJrZXItaWNvbixcclxuLmxlYWZsZXQtbWFya2VyLXNoYWRvdyB7XHJcblx0LXdlYmtpdC11c2VyLXNlbGVjdDogbm9uZTtcclxuXHQgICAtbW96LXVzZXItc2VsZWN0OiBub25lO1xyXG5cdCAgICAgICAgdXNlci1zZWxlY3Q6IG5vbmU7XHJcblx0ICAtd2Via2l0LXVzZXItZHJhZzogbm9uZTtcclxuXHR9XHJcbi8qIFByZXZlbnRzIElFMTEgZnJvbSBoaWdobGlnaHRpbmcgdGlsZXMgaW4gYmx1ZSAqL1xyXG4ubGVhZmxldC10aWxlOjpzZWxlY3Rpb24ge1xyXG5cdGJhY2tncm91bmQ6IHRyYW5zcGFyZW50O1xyXG59XHJcbi8qIFNhZmFyaSByZW5kZXJzIG5vbi1yZXRpbmEgdGlsZSBvbiByZXRpbmEgYmV0dGVyIHdpdGggdGhpcywgYnV0IENocm9tZSBpcyB3b3JzZSAqL1xyXG4ubGVhZmxldC1zYWZhcmkgLmxlYWZsZXQtdGlsZSB7XHJcblx0aW1hZ2UtcmVuZGVyaW5nOiAtd2Via2l0LW9wdGltaXplLWNvbnRyYXN0O1xyXG5cdH1cclxuLyogaGFjayB0aGF0IHByZXZlbnRzIGh3IGxheWVycyBcInN0cmV0Y2hpbmdcIiB3aGVuIGxvYWRpbmcgbmV3IHRpbGVzICovXHJcbi5sZWFmbGV0LXNhZmFyaSAubGVhZmxldC10aWxlLWNvbnRhaW5lciB7XHJcblx0d2lkdGg6IDE2MDBweDtcclxuXHRoZWlnaHQ6IDE2MDBweDtcclxuXHQtd2Via2l0LXRyYW5zZm9ybS1vcmlnaW46IDAgMDtcclxuXHR9XHJcbi5sZWFmbGV0LW1hcmtlci1pY29uLFxyXG4ubGVhZmxldC1tYXJrZXItc2hhZG93IHtcclxuXHRkaXNwbGF5OiBibG9jaztcclxuXHR9XHJcbi8qIC5sZWFmbGV0LWNvbnRhaW5lciBzdmc6IHJlc2V0IHN2ZyBtYXgtd2lkdGggZGVjbGVyYXRpb24gc2hpcHBlZCBpbiBKb29tbGEhIChqb29tbGEub3JnKSAzLnggKi9cclxuLyogLmxlYWZsZXQtY29udGFpbmVyIGltZzogbWFwIGlzIGJyb2tlbiBpbiBGRiBpZiB5b3UgaGF2ZSBtYXgtd2lkdGg6IDEwMCUgb24gdGlsZXMgKi9cclxuLmxlYWZsZXQtY29udGFpbmVyIC5sZWFmbGV0LW92ZXJsYXktcGFuZSBzdmcsXHJcbi5sZWFmbGV0LWNvbnRhaW5lciAubGVhZmxldC1tYXJrZXItcGFuZSBpbWcsXHJcbi5sZWFmbGV0LWNvbnRhaW5lciAubGVhZmxldC1zaGFkb3ctcGFuZSBpbWcsXHJcbi5sZWFmbGV0LWNvbnRhaW5lciAubGVhZmxldC10aWxlLXBhbmUgaW1nLFxyXG4ubGVhZmxldC1jb250YWluZXIgaW1nLmxlYWZsZXQtaW1hZ2UtbGF5ZXIsXHJcbi5sZWFmbGV0LWNvbnRhaW5lciAubGVhZmxldC10aWxlIHtcclxuXHRtYXgtd2lkdGg6IG5vbmUgIWltcG9ydGFudDtcclxuXHRtYXgtaGVpZ2h0OiBub25lICFpbXBvcnRhbnQ7XHJcblx0fVxyXG5cclxuLmxlYWZsZXQtY29udGFpbmVyLmxlYWZsZXQtdG91Y2gtem9vbSB7XHJcblx0LW1zLXRvdWNoLWFjdGlvbjogcGFuLXggcGFuLXk7XHJcblx0dG91Y2gtYWN0aW9uOiBwYW4teCBwYW4teTtcclxuXHR9XHJcbi5sZWFmbGV0LWNvbnRhaW5lci5sZWFmbGV0LXRvdWNoLWRyYWcge1xyXG5cdC1tcy10b3VjaC1hY3Rpb246IHBpbmNoLXpvb207XHJcblx0LyogRmFsbGJhY2sgZm9yIEZGIHdoaWNoIGRvZXNuJ3Qgc3VwcG9ydCBwaW5jaC16b29tICovXHJcblx0dG91Y2gtYWN0aW9uOiBub25lO1xyXG5cdHRvdWNoLWFjdGlvbjogcGluY2gtem9vbTtcclxufVxyXG4ubGVhZmxldC1jb250YWluZXIubGVhZmxldC10b3VjaC1kcmFnLmxlYWZsZXQtdG91Y2gtem9vbSB7XHJcblx0LW1zLXRvdWNoLWFjdGlvbjogbm9uZTtcclxuXHR0b3VjaC1hY3Rpb246IG5vbmU7XHJcbn1cclxuLmxlYWZsZXQtY29udGFpbmVyIHtcclxuXHQtd2Via2l0LXRhcC1oaWdobGlnaHQtY29sb3I6IHRyYW5zcGFyZW50O1xyXG59XHJcbi5sZWFmbGV0LWNvbnRhaW5lciBhIHtcclxuXHQtd2Via2l0LXRhcC1oaWdobGlnaHQtY29sb3I6IHJnYmEoNTEsIDE4MSwgMjI5LCAwLjQpO1xyXG59XHJcbi5sZWFmbGV0LXRpbGUge1xyXG5cdGZpbHRlcjogaW5oZXJpdDtcclxuXHR2aXNpYmlsaXR5OiBoaWRkZW47XHJcblx0fVxyXG4ubGVhZmxldC10aWxlLWxvYWRlZCB7XHJcblx0dmlzaWJpbGl0eTogaW5oZXJpdDtcclxuXHR9XHJcbi5sZWFmbGV0LXpvb20tYm94IHtcclxuXHR3aWR0aDogMDtcclxuXHRoZWlnaHQ6IDA7XHJcblx0LW1vei1ib3gtc2l6aW5nOiBib3JkZXItYm94O1xyXG5cdCAgICAgYm94LXNpemluZzogYm9yZGVyLWJveDtcclxuXHR6LWluZGV4OiA4MDA7XHJcblx0fVxyXG4vKiB3b3JrYXJvdW5kIGZvciBodHRwczovL2J1Z3ppbGxhLm1vemlsbGEub3JnL3Nob3dfYnVnLmNnaT9pZD04ODgzMTkgKi9cclxuLmxlYWZsZXQtb3ZlcmxheS1wYW5lIHN2ZyB7XHJcblx0LW1vei11c2VyLXNlbGVjdDogbm9uZTtcclxuXHR9XHJcblxyXG4ubGVhZmxldC1wYW5lICAgICAgICAgeyB6LWluZGV4OiA0MDA7IH1cclxuXHJcbi5sZWFmbGV0LXRpbGUtcGFuZSAgICB7IHotaW5kZXg6IDIwMDsgfVxyXG4ubGVhZmxldC1vdmVybGF5LXBhbmUgeyB6LWluZGV4OiA0MDA7IH1cclxuLmxlYWZsZXQtc2hhZG93LXBhbmUgIHsgei1pbmRleDogNTAwOyB9XHJcbi5sZWFmbGV0LW1hcmtlci1wYW5lICB7IHotaW5kZXg6IDYwMDsgfVxyXG4ubGVhZmxldC10b29sdGlwLXBhbmUgICB7IHotaW5kZXg6IDY1MDsgfVxyXG4ubGVhZmxldC1wb3B1cC1wYW5lICAgeyB6LWluZGV4OiA3MDA7IH1cclxuXHJcbi5sZWFmbGV0LW1hcC1wYW5lIGNhbnZhcyB7IHotaW5kZXg6IDEwMDsgfVxyXG4ubGVhZmxldC1tYXAtcGFuZSBzdmcgICAgeyB6LWluZGV4OiAyMDA7IH1cclxuXHJcbi5sZWFmbGV0LXZtbC1zaGFwZSB7XHJcblx0d2lkdGg6IDFweDtcclxuXHRoZWlnaHQ6IDFweDtcclxuXHR9XHJcbi5sdm1sIHtcclxuXHRiZWhhdmlvcjogdXJsKCNkZWZhdWx0I1ZNTCk7XHJcblx0ZGlzcGxheTogaW5saW5lLWJsb2NrO1xyXG5cdHBvc2l0aW9uOiBhYnNvbHV0ZTtcclxuXHR9XHJcblxyXG5cclxuLyogY29udHJvbCBwb3NpdGlvbmluZyAqL1xyXG5cclxuLmxlYWZsZXQtY29udHJvbCB7XHJcblx0cG9zaXRpb246IHJlbGF0aXZlO1xyXG5cdHotaW5kZXg6IDgwMDtcclxuXHRwb2ludGVyLWV2ZW50czogdmlzaWJsZVBhaW50ZWQ7IC8qIElFIDktMTAgZG9lc24ndCBoYXZlIGF1dG8gKi9cclxuXHRwb2ludGVyLWV2ZW50czogYXV0bztcclxuXHR9XHJcbi5sZWFmbGV0LXRvcCxcclxuLmxlYWZsZXQtYm90dG9tIHtcclxuXHRwb3NpdGlvbjogYWJzb2x1dGU7XHJcblx0ei1pbmRleDogMTAwMDtcclxuXHRwb2ludGVyLWV2ZW50czogbm9uZTtcclxuXHR9XHJcbi5sZWFmbGV0LXRvcCB7XHJcblx0dG9wOiAwO1xyXG5cdH1cclxuLmxlYWZsZXQtcmlnaHQge1xyXG5cdHJpZ2h0OiAwO1xyXG5cdH1cclxuLmxlYWZsZXQtYm90dG9tIHtcclxuXHRib3R0b206IDA7XHJcblx0fVxyXG4ubGVhZmxldC1sZWZ0IHtcclxuXHRsZWZ0OiAwO1xyXG5cdH1cclxuLmxlYWZsZXQtY29udHJvbCB7XHJcblx0ZmxvYXQ6IGxlZnQ7XHJcblx0Y2xlYXI6IGJvdGg7XHJcblx0fVxyXG4ubGVhZmxldC1yaWdodCAubGVhZmxldC1jb250cm9sIHtcclxuXHRmbG9hdDogcmlnaHQ7XHJcblx0fVxyXG4ubGVhZmxldC10b3AgLmxlYWZsZXQtY29udHJvbCB7XHJcblx0bWFyZ2luLXRvcDogMTBweDtcclxuXHR9XHJcbi5sZWFmbGV0LWJvdHRvbSAubGVhZmxldC1jb250cm9sIHtcclxuXHRtYXJnaW4tYm90dG9tOiAxMHB4O1xyXG5cdH1cclxuLmxlYWZsZXQtbGVmdCAubGVhZmxldC1jb250cm9sIHtcclxuXHRtYXJnaW4tbGVmdDogMTBweDtcclxuXHR9XHJcbi5sZWFmbGV0LXJpZ2h0IC5sZWFmbGV0LWNvbnRyb2wge1xyXG5cdG1hcmdpbi1yaWdodDogMTBweDtcclxuXHR9XHJcblxyXG5cclxuLyogem9vbSBhbmQgZmFkZSBhbmltYXRpb25zICovXHJcblxyXG4ubGVhZmxldC1mYWRlLWFuaW0gLmxlYWZsZXQtdGlsZSB7XHJcblx0d2lsbC1jaGFuZ2U6IG9wYWNpdHk7XHJcblx0fVxyXG4ubGVhZmxldC1mYWRlLWFuaW0gLmxlYWZsZXQtcG9wdXAge1xyXG5cdG9wYWNpdHk6IDA7XHJcblx0LXdlYmtpdC10cmFuc2l0aW9uOiBvcGFjaXR5IDAuMnMgbGluZWFyO1xyXG5cdCAgIC1tb3otdHJhbnNpdGlvbjogb3BhY2l0eSAwLjJzIGxpbmVhcjtcclxuXHQgICAgICAgIHRyYW5zaXRpb246IG9wYWNpdHkgMC4ycyBsaW5lYXI7XHJcblx0fVxyXG4ubGVhZmxldC1mYWRlLWFuaW0gLmxlYWZsZXQtbWFwLXBhbmUgLmxlYWZsZXQtcG9wdXAge1xyXG5cdG9wYWNpdHk6IDE7XHJcblx0fVxyXG4ubGVhZmxldC16b29tLWFuaW1hdGVkIHtcclxuXHQtd2Via2l0LXRyYW5zZm9ybS1vcmlnaW46IDAgMDtcclxuXHQgICAgLW1zLXRyYW5zZm9ybS1vcmlnaW46IDAgMDtcclxuXHQgICAgICAgIHRyYW5zZm9ybS1vcmlnaW46IDAgMDtcclxuXHR9XHJcbi5sZWFmbGV0LXpvb20tYW5pbSAubGVhZmxldC16b29tLWFuaW1hdGVkIHtcclxuXHR3aWxsLWNoYW5nZTogdHJhbnNmb3JtO1xyXG5cdH1cclxuLmxlYWZsZXQtem9vbS1hbmltIC5sZWFmbGV0LXpvb20tYW5pbWF0ZWQge1xyXG5cdC13ZWJraXQtdHJhbnNpdGlvbjogLXdlYmtpdC10cmFuc2Zvcm0gMC4yNXMgY3ViaWMtYmV6aWVyKDAsMCwwLjI1LDEpO1xyXG5cdCAgIC1tb3otdHJhbnNpdGlvbjogICAgLW1vei10cmFuc2Zvcm0gMC4yNXMgY3ViaWMtYmV6aWVyKDAsMCwwLjI1LDEpO1xyXG5cdCAgICAgICAgdHJhbnNpdGlvbjogICAgICAgICB0cmFuc2Zvcm0gMC4yNXMgY3ViaWMtYmV6aWVyKDAsMCwwLjI1LDEpO1xyXG5cdH1cclxuLmxlYWZsZXQtem9vbS1hbmltIC5sZWFmbGV0LXRpbGUsXHJcbi5sZWFmbGV0LXBhbi1hbmltIC5sZWFmbGV0LXRpbGUge1xyXG5cdC13ZWJraXQtdHJhbnNpdGlvbjogbm9uZTtcclxuXHQgICAtbW96LXRyYW5zaXRpb246IG5vbmU7XHJcblx0ICAgICAgICB0cmFuc2l0aW9uOiBub25lO1xyXG5cdH1cclxuXHJcbi5sZWFmbGV0LXpvb20tYW5pbSAubGVhZmxldC16b29tLWhpZGUge1xyXG5cdHZpc2liaWxpdHk6IGhpZGRlbjtcclxuXHR9XHJcblxyXG5cclxuLyogY3Vyc29ycyAqL1xyXG5cclxuLmxlYWZsZXQtaW50ZXJhY3RpdmUge1xyXG5cdGN1cnNvcjogcG9pbnRlcjtcclxuXHR9XHJcbi5sZWFmbGV0LWdyYWIge1xyXG5cdGN1cnNvcjogLXdlYmtpdC1ncmFiO1xyXG5cdGN1cnNvcjogICAgLW1vei1ncmFiO1xyXG5cdGN1cnNvcjogICAgICAgICBncmFiO1xyXG5cdH1cclxuLmxlYWZsZXQtY3Jvc3NoYWlyLFxyXG4ubGVhZmxldC1jcm9zc2hhaXIgLmxlYWZsZXQtaW50ZXJhY3RpdmUge1xyXG5cdGN1cnNvcjogY3Jvc3NoYWlyO1xyXG5cdH1cclxuLmxlYWZsZXQtcG9wdXAtcGFuZSxcclxuLmxlYWZsZXQtY29udHJvbCB7XHJcblx0Y3Vyc29yOiBhdXRvO1xyXG5cdH1cclxuLmxlYWZsZXQtZHJhZ2dpbmcgLmxlYWZsZXQtZ3JhYixcclxuLmxlYWZsZXQtZHJhZ2dpbmcgLmxlYWZsZXQtZ3JhYiAubGVhZmxldC1pbnRlcmFjdGl2ZSxcclxuLmxlYWZsZXQtZHJhZ2dpbmcgLmxlYWZsZXQtbWFya2VyLWRyYWdnYWJsZSB7XHJcblx0Y3Vyc29yOiBtb3ZlO1xyXG5cdGN1cnNvcjogLXdlYmtpdC1ncmFiYmluZztcclxuXHRjdXJzb3I6ICAgIC1tb3otZ3JhYmJpbmc7XHJcblx0Y3Vyc29yOiAgICAgICAgIGdyYWJiaW5nO1xyXG5cdH1cclxuXHJcbi8qIG1hcmtlciAmIG92ZXJsYXlzIGludGVyYWN0aXZpdHkgKi9cclxuLmxlYWZsZXQtbWFya2VyLWljb24sXHJcbi5sZWFmbGV0LW1hcmtlci1zaGFkb3csXHJcbi5sZWFmbGV0LWltYWdlLWxheWVyLFxyXG4ubGVhZmxldC1wYW5lID4gc3ZnIHBhdGgsXHJcbi5sZWFmbGV0LXRpbGUtY29udGFpbmVyIHtcclxuXHRwb2ludGVyLWV2ZW50czogbm9uZTtcclxuXHR9XHJcblxyXG4ubGVhZmxldC1tYXJrZXItaWNvbi5sZWFmbGV0LWludGVyYWN0aXZlLFxyXG4ubGVhZmxldC1pbWFnZS1sYXllci5sZWFmbGV0LWludGVyYWN0aXZlLFxyXG4ubGVhZmxldC1wYW5lID4gc3ZnIHBhdGgubGVhZmxldC1pbnRlcmFjdGl2ZSxcclxuc3ZnLmxlYWZsZXQtaW1hZ2UtbGF5ZXIubGVhZmxldC1pbnRlcmFjdGl2ZSBwYXRoIHtcclxuXHRwb2ludGVyLWV2ZW50czogdmlzaWJsZVBhaW50ZWQ7IC8qIElFIDktMTAgZG9lc24ndCBoYXZlIGF1dG8gKi9cclxuXHRwb2ludGVyLWV2ZW50czogYXV0bztcclxuXHR9XHJcblxyXG4vKiB2aXN1YWwgdHdlYWtzICovXHJcblxyXG4ubGVhZmxldC1jb250YWluZXIge1xyXG5cdGJhY2tncm91bmQ6ICNkZGQ7XHJcblx0b3V0bGluZTogMDtcclxuXHR9XHJcbi5sZWFmbGV0LWNvbnRhaW5lciBhIHtcclxuXHRjb2xvcjogIzAwNzhBODtcclxuXHR9XHJcbi5sZWFmbGV0LWNvbnRhaW5lciBhLmxlYWZsZXQtYWN0aXZlIHtcclxuXHRvdXRsaW5lOiAycHggc29saWQgb3JhbmdlO1xyXG5cdH1cclxuLmxlYWZsZXQtem9vbS1ib3gge1xyXG5cdGJvcmRlcjogMnB4IGRvdHRlZCAjMzhmO1xyXG5cdGJhY2tncm91bmQ6IHJnYmEoMjU1LDI1NSwyNTUsMC41KTtcclxuXHR9XHJcblxyXG5cclxuLyogZ2VuZXJhbCB0eXBvZ3JhcGh5ICovXHJcbi5sZWFmbGV0LWNvbnRhaW5lciB7XHJcblx0Zm9udDogMTJweC8xLjUgXCJIZWx2ZXRpY2EgTmV1ZVwiLCBBcmlhbCwgSGVsdmV0aWNhLCBzYW5zLXNlcmlmO1xyXG5cdH1cclxuXHJcblxyXG4vKiBnZW5lcmFsIHRvb2xiYXIgc3R5bGVzICovXHJcblxyXG4ubGVhZmxldC1iYXIge1xyXG5cdGJveC1zaGFkb3c6IDAgMXB4IDVweCByZ2JhKDAsMCwwLDAuNjUpO1xyXG5cdGJvcmRlci1yYWRpdXM6IDRweDtcclxuXHR9XHJcbi5sZWFmbGV0LWJhciBhLFxyXG4ubGVhZmxldC1iYXIgYTpob3ZlciB7XHJcblx0YmFja2dyb3VuZC1jb2xvcjogI2ZmZjtcclxuXHRib3JkZXItYm90dG9tOiAxcHggc29saWQgI2NjYztcclxuXHR3aWR0aDogMjZweDtcclxuXHRoZWlnaHQ6IDI2cHg7XHJcblx0bGluZS1oZWlnaHQ6IDI2cHg7XHJcblx0ZGlzcGxheTogYmxvY2s7XHJcblx0dGV4dC1hbGlnbjogY2VudGVyO1xyXG5cdHRleHQtZGVjb3JhdGlvbjogbm9uZTtcclxuXHRjb2xvcjogYmxhY2s7XHJcblx0fVxyXG4ubGVhZmxldC1iYXIgYSxcclxuLmxlYWZsZXQtY29udHJvbC1sYXllcnMtdG9nZ2xlIHtcclxuXHRiYWNrZ3JvdW5kLXBvc2l0aW9uOiA1MCUgNTAlO1xyXG5cdGJhY2tncm91bmQtcmVwZWF0OiBuby1yZXBlYXQ7XHJcblx0ZGlzcGxheTogYmxvY2s7XHJcblx0fVxyXG4ubGVhZmxldC1iYXIgYTpob3ZlciB7XHJcblx0YmFja2dyb3VuZC1jb2xvcjogI2Y0ZjRmNDtcclxuXHR9XHJcbi5sZWFmbGV0LWJhciBhOmZpcnN0LWNoaWxkIHtcclxuXHRib3JkZXItdG9wLWxlZnQtcmFkaXVzOiA0cHg7XHJcblx0Ym9yZGVyLXRvcC1yaWdodC1yYWRpdXM6IDRweDtcclxuXHR9XHJcbi5sZWFmbGV0LWJhciBhOmxhc3QtY2hpbGQge1xyXG5cdGJvcmRlci1ib3R0b20tbGVmdC1yYWRpdXM6IDRweDtcclxuXHRib3JkZXItYm90dG9tLXJpZ2h0LXJhZGl1czogNHB4O1xyXG5cdGJvcmRlci1ib3R0b206IG5vbmU7XHJcblx0fVxyXG4ubGVhZmxldC1iYXIgYS5sZWFmbGV0LWRpc2FibGVkIHtcclxuXHRjdXJzb3I6IGRlZmF1bHQ7XHJcblx0YmFja2dyb3VuZC1jb2xvcjogI2Y0ZjRmNDtcclxuXHRjb2xvcjogI2JiYjtcclxuXHR9XHJcblxyXG4ubGVhZmxldC10b3VjaCAubGVhZmxldC1iYXIgYSB7XHJcblx0d2lkdGg6IDMwcHg7XHJcblx0aGVpZ2h0OiAzMHB4O1xyXG5cdGxpbmUtaGVpZ2h0OiAzMHB4O1xyXG5cdH1cclxuLmxlYWZsZXQtdG91Y2ggLmxlYWZsZXQtYmFyIGE6Zmlyc3QtY2hpbGQge1xyXG5cdGJvcmRlci10b3AtbGVmdC1yYWRpdXM6IDJweDtcclxuXHRib3JkZXItdG9wLXJpZ2h0LXJhZGl1czogMnB4O1xyXG5cdH1cclxuLmxlYWZsZXQtdG91Y2ggLmxlYWZsZXQtYmFyIGE6bGFzdC1jaGlsZCB7XHJcblx0Ym9yZGVyLWJvdHRvbS1sZWZ0LXJhZGl1czogMnB4O1xyXG5cdGJvcmRlci1ib3R0b20tcmlnaHQtcmFkaXVzOiAycHg7XHJcblx0fVxyXG5cclxuLyogem9vbSBjb250cm9sICovXHJcblxyXG4ubGVhZmxldC1jb250cm9sLXpvb20taW4sXHJcbi5sZWFmbGV0LWNvbnRyb2wtem9vbS1vdXQge1xyXG5cdGZvbnQ6IGJvbGQgMThweCAnTHVjaWRhIENvbnNvbGUnLCBNb25hY28sIG1vbm9zcGFjZTtcclxuXHR0ZXh0LWluZGVudDogMXB4O1xyXG5cdH1cclxuXHJcbi5sZWFmbGV0LXRvdWNoIC5sZWFmbGV0LWNvbnRyb2wtem9vbS1pbiwgLmxlYWZsZXQtdG91Y2ggLmxlYWZsZXQtY29udHJvbC16b29tLW91dCAge1xyXG5cdGZvbnQtc2l6ZTogMjJweDtcclxuXHR9XHJcblxyXG5cclxuLyogbGF5ZXJzIGNvbnRyb2wgKi9cclxuXHJcbi5sZWFmbGV0LWNvbnRyb2wtbGF5ZXJzIHtcclxuXHRib3gtc2hhZG93OiAwIDFweCA1cHggcmdiYSgwLDAsMCwwLjQpO1xyXG5cdGJhY2tncm91bmQ6ICNmZmY7XHJcblx0Ym9yZGVyLXJhZGl1czogNXB4O1xyXG5cdH1cclxuLmxlYWZsZXQtY29udHJvbC1sYXllcnMtdG9nZ2xlIHtcclxuXHRiYWNrZ3JvdW5kLWltYWdlOiB1cmwoaW1hZ2VzL2xheWVycy5wbmcpO1xyXG5cdHdpZHRoOiAzNnB4O1xyXG5cdGhlaWdodDogMzZweDtcclxuXHR9XHJcbi5sZWFmbGV0LXJldGluYSAubGVhZmxldC1jb250cm9sLWxheWVycy10b2dnbGUge1xyXG5cdGJhY2tncm91bmQtaW1hZ2U6IHVybChpbWFnZXMvbGF5ZXJzLTJ4LnBuZyk7XHJcblx0YmFja2dyb3VuZC1zaXplOiAyNnB4IDI2cHg7XHJcblx0fVxyXG4ubGVhZmxldC10b3VjaCAubGVhZmxldC1jb250cm9sLWxheWVycy10b2dnbGUge1xyXG5cdHdpZHRoOiA0NHB4O1xyXG5cdGhlaWdodDogNDRweDtcclxuXHR9XHJcbi5sZWFmbGV0LWNvbnRyb2wtbGF5ZXJzIC5sZWFmbGV0LWNvbnRyb2wtbGF5ZXJzLWxpc3QsXHJcbi5sZWFmbGV0LWNvbnRyb2wtbGF5ZXJzLWV4cGFuZGVkIC5sZWFmbGV0LWNvbnRyb2wtbGF5ZXJzLXRvZ2dsZSB7XHJcblx0ZGlzcGxheTogbm9uZTtcclxuXHR9XHJcbi5sZWFmbGV0LWNvbnRyb2wtbGF5ZXJzLWV4cGFuZGVkIC5sZWFmbGV0LWNvbnRyb2wtbGF5ZXJzLWxpc3Qge1xyXG5cdGRpc3BsYXk6IGJsb2NrO1xyXG5cdHBvc2l0aW9uOiByZWxhdGl2ZTtcclxuXHR9XHJcbi5sZWFmbGV0LWNvbnRyb2wtbGF5ZXJzLWV4cGFuZGVkIHtcclxuXHRwYWRkaW5nOiA2cHggMTBweCA2cHggNnB4O1xyXG5cdGNvbG9yOiAjMzMzO1xyXG5cdGJhY2tncm91bmQ6ICNmZmY7XHJcblx0fVxyXG4ubGVhZmxldC1jb250cm9sLWxheWVycy1zY3JvbGxiYXIge1xyXG5cdG92ZXJmbG93LXk6IHNjcm9sbDtcclxuXHRvdmVyZmxvdy14OiBoaWRkZW47XHJcblx0cGFkZGluZy1yaWdodDogNXB4O1xyXG5cdH1cclxuLmxlYWZsZXQtY29udHJvbC1sYXllcnMtc2VsZWN0b3Ige1xyXG5cdG1hcmdpbi10b3A6IDJweDtcclxuXHRwb3NpdGlvbjogcmVsYXRpdmU7XHJcblx0dG9wOiAxcHg7XHJcblx0fVxyXG4ubGVhZmxldC1jb250cm9sLWxheWVycyBsYWJlbCB7XHJcblx0ZGlzcGxheTogYmxvY2s7XHJcblx0fVxyXG4ubGVhZmxldC1jb250cm9sLWxheWVycy1zZXBhcmF0b3Ige1xyXG5cdGhlaWdodDogMDtcclxuXHRib3JkZXItdG9wOiAxcHggc29saWQgI2RkZDtcclxuXHRtYXJnaW46IDVweCAtMTBweCA1cHggLTZweDtcclxuXHR9XHJcblxyXG4vKiBEZWZhdWx0IGljb24gVVJMcyAqL1xyXG4ubGVhZmxldC1kZWZhdWx0LWljb24tcGF0aCB7XHJcblx0YmFja2dyb3VuZC1pbWFnZTogdXJsKGltYWdlcy9tYXJrZXItaWNvbi5wbmcpO1xyXG5cdH1cclxuXHJcblxyXG4vKiBhdHRyaWJ1dGlvbiBhbmQgc2NhbGUgY29udHJvbHMgKi9cclxuXHJcbi5sZWFmbGV0LWNvbnRhaW5lciAubGVhZmxldC1jb250cm9sLWF0dHJpYnV0aW9uIHtcclxuXHRiYWNrZ3JvdW5kOiAjZmZmO1xyXG5cdGJhY2tncm91bmQ6IHJnYmEoMjU1LCAyNTUsIDI1NSwgMC43KTtcclxuXHRtYXJnaW46IDA7XHJcblx0fVxyXG4ubGVhZmxldC1jb250cm9sLWF0dHJpYnV0aW9uLFxyXG4ubGVhZmxldC1jb250cm9sLXNjYWxlLWxpbmUge1xyXG5cdHBhZGRpbmc6IDAgNXB4O1xyXG5cdGNvbG9yOiAjMzMzO1xyXG5cdH1cclxuLmxlYWZsZXQtY29udHJvbC1hdHRyaWJ1dGlvbiBhIHtcclxuXHR0ZXh0LWRlY29yYXRpb246IG5vbmU7XHJcblx0fVxyXG4ubGVhZmxldC1jb250cm9sLWF0dHJpYnV0aW9uIGE6aG92ZXIge1xyXG5cdHRleHQtZGVjb3JhdGlvbjogdW5kZXJsaW5lO1xyXG5cdH1cclxuLmxlYWZsZXQtY29udGFpbmVyIC5sZWFmbGV0LWNvbnRyb2wtYXR0cmlidXRpb24sXHJcbi5sZWFmbGV0LWNvbnRhaW5lciAubGVhZmxldC1jb250cm9sLXNjYWxlIHtcclxuXHRmb250LXNpemU6IDExcHg7XHJcblx0fVxyXG4ubGVhZmxldC1sZWZ0IC5sZWFmbGV0LWNvbnRyb2wtc2NhbGUge1xyXG5cdG1hcmdpbi1sZWZ0OiA1cHg7XHJcblx0fVxyXG4ubGVhZmxldC1ib3R0b20gLmxlYWZsZXQtY29udHJvbC1zY2FsZSB7XHJcblx0bWFyZ2luLWJvdHRvbTogNXB4O1xyXG5cdH1cclxuLmxlYWZsZXQtY29udHJvbC1zY2FsZS1saW5lIHtcclxuXHRib3JkZXI6IDJweCBzb2xpZCAjNzc3O1xyXG5cdGJvcmRlci10b3A6IG5vbmU7XHJcblx0bGluZS1oZWlnaHQ6IDEuMTtcclxuXHRwYWRkaW5nOiAycHggNXB4IDFweDtcclxuXHRmb250LXNpemU6IDExcHg7XHJcblx0d2hpdGUtc3BhY2U6IG5vd3JhcDtcclxuXHRvdmVyZmxvdzogaGlkZGVuO1xyXG5cdC1tb3otYm94LXNpemluZzogYm9yZGVyLWJveDtcclxuXHQgICAgIGJveC1zaXppbmc6IGJvcmRlci1ib3g7XHJcblxyXG5cdGJhY2tncm91bmQ6ICNmZmY7XHJcblx0YmFja2dyb3VuZDogcmdiYSgyNTUsIDI1NSwgMjU1LCAwLjUpO1xyXG5cdH1cclxuLmxlYWZsZXQtY29udHJvbC1zY2FsZS1saW5lOm5vdCg6Zmlyc3QtY2hpbGQpIHtcclxuXHRib3JkZXItdG9wOiAycHggc29saWQgIzc3NztcclxuXHRib3JkZXItYm90dG9tOiBub25lO1xyXG5cdG1hcmdpbi10b3A6IC0ycHg7XHJcblx0fVxyXG4ubGVhZmxldC1jb250cm9sLXNjYWxlLWxpbmU6bm90KDpmaXJzdC1jaGlsZCk6bm90KDpsYXN0LWNoaWxkKSB7XHJcblx0Ym9yZGVyLWJvdHRvbTogMnB4IHNvbGlkICM3Nzc7XHJcblx0fVxyXG5cclxuLmxlYWZsZXQtdG91Y2ggLmxlYWZsZXQtY29udHJvbC1hdHRyaWJ1dGlvbixcclxuLmxlYWZsZXQtdG91Y2ggLmxlYWZsZXQtY29udHJvbC1sYXllcnMsXHJcbi5sZWFmbGV0LXRvdWNoIC5sZWFmbGV0LWJhciB7XHJcblx0Ym94LXNoYWRvdzogbm9uZTtcclxuXHR9XHJcbi5sZWFmbGV0LXRvdWNoIC5sZWFmbGV0LWNvbnRyb2wtbGF5ZXJzLFxyXG4ubGVhZmxldC10b3VjaCAubGVhZmxldC1iYXIge1xyXG5cdGJvcmRlcjogMnB4IHNvbGlkIHJnYmEoMCwwLDAsMC4yKTtcclxuXHRiYWNrZ3JvdW5kLWNsaXA6IHBhZGRpbmctYm94O1xyXG5cdH1cclxuXHJcblxyXG4vKiBwb3B1cCAqL1xyXG5cclxuLmxlYWZsZXQtcG9wdXAge1xyXG5cdHBvc2l0aW9uOiBhYnNvbHV0ZTtcclxuXHR0ZXh0LWFsaWduOiBjZW50ZXI7XHJcblx0bWFyZ2luLWJvdHRvbTogMjBweDtcclxuXHR9XHJcbi5sZWFmbGV0LXBvcHVwLWNvbnRlbnQtd3JhcHBlciB7XHJcblx0cGFkZGluZzogMXB4O1xyXG5cdHRleHQtYWxpZ246IGxlZnQ7XHJcblx0Ym9yZGVyLXJhZGl1czogMTJweDtcclxuXHR9XHJcbi5sZWFmbGV0LXBvcHVwLWNvbnRlbnQge1xyXG5cdG1hcmdpbjogMTNweCAxOXB4O1xyXG5cdGxpbmUtaGVpZ2h0OiAxLjQ7XHJcblx0fVxyXG4ubGVhZmxldC1wb3B1cC1jb250ZW50IHAge1xyXG5cdG1hcmdpbjogMThweCAwO1xyXG5cdH1cclxuLmxlYWZsZXQtcG9wdXAtdGlwLWNvbnRhaW5lciB7XHJcblx0d2lkdGg6IDQwcHg7XHJcblx0aGVpZ2h0OiAyMHB4O1xyXG5cdHBvc2l0aW9uOiBhYnNvbHV0ZTtcclxuXHRsZWZ0OiA1MCU7XHJcblx0bWFyZ2luLWxlZnQ6IC0yMHB4O1xyXG5cdG92ZXJmbG93OiBoaWRkZW47XHJcblx0cG9pbnRlci1ldmVudHM6IG5vbmU7XHJcblx0fVxyXG4ubGVhZmxldC1wb3B1cC10aXAge1xyXG5cdHdpZHRoOiAxN3B4O1xyXG5cdGhlaWdodDogMTdweDtcclxuXHRwYWRkaW5nOiAxcHg7XHJcblxyXG5cdG1hcmdpbjogLTEwcHggYXV0byAwO1xyXG5cclxuXHQtd2Via2l0LXRyYW5zZm9ybTogcm90YXRlKDQ1ZGVnKTtcclxuXHQgICAtbW96LXRyYW5zZm9ybTogcm90YXRlKDQ1ZGVnKTtcclxuXHQgICAgLW1zLXRyYW5zZm9ybTogcm90YXRlKDQ1ZGVnKTtcclxuXHQgICAgICAgIHRyYW5zZm9ybTogcm90YXRlKDQ1ZGVnKTtcclxuXHR9XHJcbi5sZWFmbGV0LXBvcHVwLWNvbnRlbnQtd3JhcHBlcixcclxuLmxlYWZsZXQtcG9wdXAtdGlwIHtcclxuXHRiYWNrZ3JvdW5kOiB3aGl0ZTtcclxuXHRjb2xvcjogIzMzMztcclxuXHRib3gtc2hhZG93OiAwIDNweCAxNHB4IHJnYmEoMCwwLDAsMC40KTtcclxuXHR9XHJcbi5sZWFmbGV0LWNvbnRhaW5lciBhLmxlYWZsZXQtcG9wdXAtY2xvc2UtYnV0dG9uIHtcclxuXHRwb3NpdGlvbjogYWJzb2x1dGU7XHJcblx0dG9wOiAwO1xyXG5cdHJpZ2h0OiAwO1xyXG5cdHBhZGRpbmc6IDRweCA0cHggMCAwO1xyXG5cdGJvcmRlcjogbm9uZTtcclxuXHR0ZXh0LWFsaWduOiBjZW50ZXI7XHJcblx0d2lkdGg6IDE4cHg7XHJcblx0aGVpZ2h0OiAxNHB4O1xyXG5cdGZvbnQ6IDE2cHgvMTRweCBUYWhvbWEsIFZlcmRhbmEsIHNhbnMtc2VyaWY7XHJcblx0Y29sb3I6ICNjM2MzYzM7XHJcblx0dGV4dC1kZWNvcmF0aW9uOiBub25lO1xyXG5cdGZvbnQtd2VpZ2h0OiBib2xkO1xyXG5cdGJhY2tncm91bmQ6IHRyYW5zcGFyZW50O1xyXG5cdH1cclxuLmxlYWZsZXQtY29udGFpbmVyIGEubGVhZmxldC1wb3B1cC1jbG9zZS1idXR0b246aG92ZXIge1xyXG5cdGNvbG9yOiAjOTk5O1xyXG5cdH1cclxuLmxlYWZsZXQtcG9wdXAtc2Nyb2xsZWQge1xyXG5cdG92ZXJmbG93OiBhdXRvO1xyXG5cdGJvcmRlci1ib3R0b206IDFweCBzb2xpZCAjZGRkO1xyXG5cdGJvcmRlci10b3A6IDFweCBzb2xpZCAjZGRkO1xyXG5cdH1cclxuXHJcbi5sZWFmbGV0LW9sZGllIC5sZWFmbGV0LXBvcHVwLWNvbnRlbnQtd3JhcHBlciB7XHJcblx0em9vbTogMTtcclxuXHR9XHJcbi5sZWFmbGV0LW9sZGllIC5sZWFmbGV0LXBvcHVwLXRpcCB7XHJcblx0d2lkdGg6IDI0cHg7XHJcblx0bWFyZ2luOiAwIGF1dG87XHJcblxyXG5cdC1tcy1maWx0ZXI6IFwicHJvZ2lkOkRYSW1hZ2VUcmFuc2Zvcm0uTWljcm9zb2Z0Lk1hdHJpeChNMTE9MC43MDcxMDY3OCwgTTEyPTAuNzA3MTA2NzgsIE0yMT0tMC43MDcxMDY3OCwgTTIyPTAuNzA3MTA2NzgpXCI7XHJcblx0ZmlsdGVyOiBwcm9naWQ6RFhJbWFnZVRyYW5zZm9ybS5NaWNyb3NvZnQuTWF0cml4KE0xMT0wLjcwNzEwNjc4LCBNMTI9MC43MDcxMDY3OCwgTTIxPS0wLjcwNzEwNjc4LCBNMjI9MC43MDcxMDY3OCk7XHJcblx0fVxyXG4ubGVhZmxldC1vbGRpZSAubGVhZmxldC1wb3B1cC10aXAtY29udGFpbmVyIHtcclxuXHRtYXJnaW4tdG9wOiAtMXB4O1xyXG5cdH1cclxuXHJcbi5sZWFmbGV0LW9sZGllIC5sZWFmbGV0LWNvbnRyb2wtem9vbSxcclxuLmxlYWZsZXQtb2xkaWUgLmxlYWZsZXQtY29udHJvbC1sYXllcnMsXHJcbi5sZWFmbGV0LW9sZGllIC5sZWFmbGV0LXBvcHVwLWNvbnRlbnQtd3JhcHBlcixcclxuLmxlYWZsZXQtb2xkaWUgLmxlYWZsZXQtcG9wdXAtdGlwIHtcclxuXHRib3JkZXI6IDFweCBzb2xpZCAjOTk5O1xyXG5cdH1cclxuXHJcblxyXG4vKiBkaXYgaWNvbiAqL1xyXG5cclxuLmxlYWZsZXQtZGl2LWljb24ge1xyXG5cdGJhY2tncm91bmQ6ICNmZmY7XHJcblx0Ym9yZGVyOiAxcHggc29saWQgIzY2NjtcclxuXHR9XHJcblxyXG5cclxuLyogVG9vbHRpcCAqL1xyXG4vKiBCYXNlIHN0eWxlcyBmb3IgdGhlIGVsZW1lbnQgdGhhdCBoYXMgYSB0b29sdGlwICovXHJcbi5sZWFmbGV0LXRvb2x0aXAge1xyXG5cdHBvc2l0aW9uOiBhYnNvbHV0ZTtcclxuXHRwYWRkaW5nOiA2cHg7XHJcblx0YmFja2dyb3VuZC1jb2xvcjogI2ZmZjtcclxuXHRib3JkZXI6IDFweCBzb2xpZCAjZmZmO1xyXG5cdGJvcmRlci1yYWRpdXM6IDNweDtcclxuXHRjb2xvcjogIzIyMjtcclxuXHR3aGl0ZS1zcGFjZTogbm93cmFwO1xyXG5cdC13ZWJraXQtdXNlci1zZWxlY3Q6IG5vbmU7XHJcblx0LW1vei11c2VyLXNlbGVjdDogbm9uZTtcclxuXHQtbXMtdXNlci1zZWxlY3Q6IG5vbmU7XHJcblx0dXNlci1zZWxlY3Q6IG5vbmU7XHJcblx0cG9pbnRlci1ldmVudHM6IG5vbmU7XHJcblx0Ym94LXNoYWRvdzogMCAxcHggM3B4IHJnYmEoMCwwLDAsMC40KTtcclxuXHR9XHJcbi5sZWFmbGV0LXRvb2x0aXAubGVhZmxldC1jbGlja2FibGUge1xyXG5cdGN1cnNvcjogcG9pbnRlcjtcclxuXHRwb2ludGVyLWV2ZW50czogYXV0bztcclxuXHR9XHJcbi5sZWFmbGV0LXRvb2x0aXAtdG9wOmJlZm9yZSxcclxuLmxlYWZsZXQtdG9vbHRpcC1ib3R0b206YmVmb3JlLFxyXG4ubGVhZmxldC10b29sdGlwLWxlZnQ6YmVmb3JlLFxyXG4ubGVhZmxldC10b29sdGlwLXJpZ2h0OmJlZm9yZSB7XHJcblx0cG9zaXRpb246IGFic29sdXRlO1xyXG5cdHBvaW50ZXItZXZlbnRzOiBub25lO1xyXG5cdGJvcmRlcjogNnB4IHNvbGlkIHRyYW5zcGFyZW50O1xyXG5cdGJhY2tncm91bmQ6IHRyYW5zcGFyZW50O1xyXG5cdGNvbnRlbnQ6IFwiXCI7XHJcblx0fVxyXG5cclxuLyogRGlyZWN0aW9ucyAqL1xyXG5cclxuLmxlYWZsZXQtdG9vbHRpcC1ib3R0b20ge1xyXG5cdG1hcmdpbi10b3A6IDZweDtcclxufVxyXG4ubGVhZmxldC10b29sdGlwLXRvcCB7XHJcblx0bWFyZ2luLXRvcDogLTZweDtcclxufVxyXG4ubGVhZmxldC10b29sdGlwLWJvdHRvbTpiZWZvcmUsXHJcbi5sZWFmbGV0LXRvb2x0aXAtdG9wOmJlZm9yZSB7XHJcblx0bGVmdDogNTAlO1xyXG5cdG1hcmdpbi1sZWZ0OiAtNnB4O1xyXG5cdH1cclxuLmxlYWZsZXQtdG9vbHRpcC10b3A6YmVmb3JlIHtcclxuXHRib3R0b206IDA7XHJcblx0bWFyZ2luLWJvdHRvbTogLTEycHg7XHJcblx0Ym9yZGVyLXRvcC1jb2xvcjogI2ZmZjtcclxuXHR9XHJcbi5sZWFmbGV0LXRvb2x0aXAtYm90dG9tOmJlZm9yZSB7XHJcblx0dG9wOiAwO1xyXG5cdG1hcmdpbi10b3A6IC0xMnB4O1xyXG5cdG1hcmdpbi1sZWZ0OiAtNnB4O1xyXG5cdGJvcmRlci1ib3R0b20tY29sb3I6ICNmZmY7XHJcblx0fVxyXG4ubGVhZmxldC10b29sdGlwLWxlZnQge1xyXG5cdG1hcmdpbi1sZWZ0OiAtNnB4O1xyXG59XHJcbi5sZWFmbGV0LXRvb2x0aXAtcmlnaHQge1xyXG5cdG1hcmdpbi1sZWZ0OiA2cHg7XHJcbn1cclxuLmxlYWZsZXQtdG9vbHRpcC1sZWZ0OmJlZm9yZSxcclxuLmxlYWZsZXQtdG9vbHRpcC1yaWdodDpiZWZvcmUge1xyXG5cdHRvcDogNTAlO1xyXG5cdG1hcmdpbi10b3A6IC02cHg7XHJcblx0fVxyXG4ubGVhZmxldC10b29sdGlwLWxlZnQ6YmVmb3JlIHtcclxuXHRyaWdodDogMDtcclxuXHRtYXJnaW4tcmlnaHQ6IC0xMnB4O1xyXG5cdGJvcmRlci1sZWZ0LWNvbG9yOiAjZmZmO1xyXG5cdH1cclxuLmxlYWZsZXQtdG9vbHRpcC1yaWdodDpiZWZvcmUge1xyXG5cdGxlZnQ6IDA7XHJcblx0bWFyZ2luLWxlZnQ6IC0xMnB4O1xyXG5cdGJvcmRlci1yaWdodC1jb2xvcjogI2ZmZjtcclxuXHR9XHJcbiJdfQ== */", '', '']]

/***/ }),

/***/ "./node_modules/leaflet/dist/leaflet.css":
/*!***********************************************!*\
  !*** ./node_modules/leaflet/dist/leaflet.css ***!
  \***********************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {


var content = __webpack_require__(/*! !../../@angular-devkit/build-angular/src/angular-cli-files/plugins/raw-css-loader.js!../../postcss-loader/src??embedded!./leaflet.css */ "./node_modules/@angular-devkit/build-angular/src/angular-cli-files/plugins/raw-css-loader.js!./node_modules/postcss-loader/src/index.js?!./node_modules/leaflet/dist/leaflet.css");

if(typeof content === 'string') content = [[module.i, content, '']];

var transform;
var insertInto;



var options = {"hmr":true}

options.transform = transform
options.insertInto = undefined;

var update = __webpack_require__(/*! ../../style-loader/lib/addStyles.js */ "./node_modules/style-loader/lib/addStyles.js")(content, options);

if(content.locals) module.exports = content.locals;

if(false) {}

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/app.component.html":
/*!**************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/app.component.html ***!
  \**************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<!--The content below is only a placeholder and can be replaced.-->\n\n<app-search-bar></app-search-bar>\n<app-location-name-display></app-location-name-display>\n<app-heatmap></app-heatmap>\n<app-sidebar></app-sidebar>\n<app-time-series></app-time-series>\n\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/map/heatmap/heatmap.component.html":
/*!******************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/map/heatmap/heatmap.component.html ***!
  \******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div id=\"map\">\n\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/map/location-name-display/location-name-display.component.html":
/*!**********************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/map/location-name-display/location-name-display.component.html ***!
  \**********************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div id=\"info\">location name:</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/map/search-bar/search.component.html":
/*!********************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/map/search-bar/search.component.html ***!
  \********************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<form class=\"example-form\" ngFormOptions=\"\">\n    <mat-form-field class=\"example-full-width\">\n        <input (keyup)=\"dropDownHandler($event)\"\n               [formControl]=\"formControl\" [matAutocomplete]=\"auto\" aria-label=\"Number\"\n               matInput placeholder=\"\"\n               id=\"search-input-id\"\n               type=\"text\">\n        <mat-placeholder id=\"placeholder\" style=\"color:#4265ff;\">Enter the location here</mat-placeholder>\n        <mat-autocomplete #auto=\"matAutocomplete\" (optionSelected)='selected($event.option.id,$event.option.value)'><br>\n            <mat-option *ngFor=\"let state of dataToDropDownMenu\" [id]=\"state.id\" [value]=\"state.value\">\n                {{state.display}}\n            </mat-option>\n        </mat-autocomplete>\n    </mat-form-field>\n</form>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/map/sidebar/sidebar.component.html":
/*!******************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/map/sidebar/sidebar.component.html ***!
  \******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div id=\"sidebar\">\n    <h4>Current Pos</h4>\n    <p id=\"mousePosition\"></p>\n\n    <!--    <h4>Start Live Tweet</h4>-->\n    <!-- LiveTweet switch -->\n    <!--    <label class=\"switch\">-->\n    <!--        <input id=\"liveTweetSwitch\" type=\"checkbox\">-->\n    <!--        <span class=\"slider round\"></span>-->\n    <!--    </label>-->\n    <app-temperature-range-slider></app-temperature-range-slider>\n</div>"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/map/sidebar/temperature-range-slider/temperature-range-slider.component.html":
/*!************************************************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/map/sidebar/temperature-range-slider/temperature-range-slider.component.html ***!
  \************************************************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<script src=\"https://code.jquery.com/jquery-1.12.4.js\"></script>\n<script src=\"https://code.jquery.com/ui/1.12.1/jquery-ui.js\"></script>\n<link rel=\"stylesheet\" href=\"//code.jquery.com/ui/1.12.1/themes/base/jquery-ui.css\">\n<div id=\"wrapper\">\n\n    <!-- Uncomment this part to show the thermometer-->\n    <div id=\"thermometer\">\n        <div id=\"temperature\" style=\"height:0\" data-value=\"0°C\"></div>\n        <div id=\"graduations\"></div>\n    </div>\n\n    <h5></h5>\n    <div id=\"temperatureSelectForm\">\n        <span>\n        <div class=\"range\">\n            <input class=\"tempLabel\" name=\"minTemp\" style=\"width:48px\" type=\"text\" value=\"Max:-6\">\n            <input (click)=\"highTemperatureSelectorUpdate($event)\" class=\"tempselect\" max=\"35\" min=\"-6\" type=\"range\"\n                   value=\"20\">\n            <input class=\"tempLabel\" name=\"maxTemp\" style=\"width:16px\" type=\"text\" value=\"35\">\n        </div>\n        <p class=\"unit\">Celsius C°</p>\n        </span>\n        <span>\n        <div class=\"range\">\n            <input class=\"tempLabel\" name=\"minTemp\" style=\"width:46px\" type=\"text\" value=\"Min:-6\">\n            <input (click)=\"lowTemperatureSelectorUpdate($event)\" class=\"tempselect\" max=\"35\" min=\"-6\" type=\"range\"\n                   value=\"20\">\n            <input class=\"tempLabel\" name=\"maxTemp\" style=\"width:16px\" type=\"text\" value=\"35\">\n        </div>\n        <p class=\"unit\">Celsius C°</p>\n        </span>\n    </div>\n\n    <div class='range-box'>\n        <div id=\"slider\"></div>\n    </div>\n</div>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/map/tab/tab.component.html":
/*!**********************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/map/tab/tab.component.html ***!
  \**********************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<mat-tab-group>\n    <mat-tab label=\"First\"> Content 1</mat-tab>\n    <mat-tab label=\"Second\"> Content 2</mat-tab>\n    <mat-tab label=\"Third\"> Content 3</mat-tab>\n</mat-tab-group>\n"

/***/ }),

/***/ "./node_modules/raw-loader/index.js!./src/app/map/time-series/time-series.component.html":
/*!**************************************************************************************!*\
  !*** ./node_modules/raw-loader!./src/app/map/time-series/time-series.component.html ***!
  \**************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "<div id='timebar-container'></div>\n<div id='report'></div>"

/***/ }),

/***/ "./node_modules/style-loader/lib/addStyles.js":
/*!****************************************************!*\
  !*** ./node_modules/style-loader/lib/addStyles.js ***!
  \****************************************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

/*
	MIT License http://www.opensource.org/licenses/mit-license.php
	Author Tobias Koppers @sokra
*/

var stylesInDom = {};

var	memoize = function (fn) {
	var memo;

	return function () {
		if (typeof memo === "undefined") memo = fn.apply(this, arguments);
		return memo;
	};
};

var isOldIE = memoize(function () {
	// Test for IE <= 9 as proposed by Browserhacks
	// @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
	// Tests for existence of standard globals is to allow style-loader
	// to operate correctly into non-standard environments
	// @see https://github.com/webpack-contrib/style-loader/issues/177
	return window && document && document.all && !window.atob;
});

var getTarget = function (target, parent) {
  if (parent){
    return parent.querySelector(target);
  }
  return document.querySelector(target);
};

var getElement = (function (fn) {
	var memo = {};

	return function(target, parent) {
                // If passing function in options, then use it for resolve "head" element.
                // Useful for Shadow Root style i.e
                // {
                //   insertInto: function () { return document.querySelector("#foo").shadowRoot }
                // }
                if (typeof target === 'function') {
                        return target();
                }
                if (typeof memo[target] === "undefined") {
			var styleTarget = getTarget.call(this, target, parent);
			// Special case to return head of iframe instead of iframe itself
			if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
				try {
					// This will throw an exception if access to iframe is blocked
					// due to cross-origin restrictions
					styleTarget = styleTarget.contentDocument.head;
				} catch(e) {
					styleTarget = null;
				}
			}
			memo[target] = styleTarget;
		}
		return memo[target]
	};
})();

var singleton = null;
var	singletonCounter = 0;
var	stylesInsertedAtTop = [];

var	fixUrls = __webpack_require__(/*! ./urls */ "./node_modules/style-loader/lib/urls.js");

module.exports = function(list, options) {
	if (typeof DEBUG !== "undefined" && DEBUG) {
		if (typeof document !== "object") throw new Error("The style-loader cannot be used in a non-browser environment");
	}

	options = options || {};

	options.attrs = typeof options.attrs === "object" ? options.attrs : {};

	// Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
	// tags it will allow on a page
	if (!options.singleton && typeof options.singleton !== "boolean") options.singleton = isOldIE();

	// By default, add <style> tags to the <head> element
        if (!options.insertInto) options.insertInto = "head";

	// By default, add <style> tags to the bottom of the target
	if (!options.insertAt) options.insertAt = "bottom";

	var styles = listToStyles(list, options);

	addStylesToDom(styles, options);

	return function update (newList) {
		var mayRemove = [];

		for (var i = 0; i < styles.length; i++) {
			var item = styles[i];
			var domStyle = stylesInDom[item.id];

			domStyle.refs--;
			mayRemove.push(domStyle);
		}

		if(newList) {
			var newStyles = listToStyles(newList, options);
			addStylesToDom(newStyles, options);
		}

		for (var i = 0; i < mayRemove.length; i++) {
			var domStyle = mayRemove[i];

			if(domStyle.refs === 0) {
				for (var j = 0; j < domStyle.parts.length; j++) domStyle.parts[j]();

				delete stylesInDom[domStyle.id];
			}
		}
	};
};

function addStylesToDom (styles, options) {
	for (var i = 0; i < styles.length; i++) {
		var item = styles[i];
		var domStyle = stylesInDom[item.id];

		if(domStyle) {
			domStyle.refs++;

			for(var j = 0; j < domStyle.parts.length; j++) {
				domStyle.parts[j](item.parts[j]);
			}

			for(; j < item.parts.length; j++) {
				domStyle.parts.push(addStyle(item.parts[j], options));
			}
		} else {
			var parts = [];

			for(var j = 0; j < item.parts.length; j++) {
				parts.push(addStyle(item.parts[j], options));
			}

			stylesInDom[item.id] = {id: item.id, refs: 1, parts: parts};
		}
	}
}

function listToStyles (list, options) {
	var styles = [];
	var newStyles = {};

	for (var i = 0; i < list.length; i++) {
		var item = list[i];
		var id = options.base ? item[0] + options.base : item[0];
		var css = item[1];
		var media = item[2];
		var sourceMap = item[3];
		var part = {css: css, media: media, sourceMap: sourceMap};

		if(!newStyles[id]) styles.push(newStyles[id] = {id: id, parts: [part]});
		else newStyles[id].parts.push(part);
	}

	return styles;
}

function insertStyleElement (options, style) {
	var target = getElement(options.insertInto)

	if (!target) {
		throw new Error("Couldn't find a style target. This probably means that the value for the 'insertInto' parameter is invalid.");
	}

	var lastStyleElementInsertedAtTop = stylesInsertedAtTop[stylesInsertedAtTop.length - 1];

	if (options.insertAt === "top") {
		if (!lastStyleElementInsertedAtTop) {
			target.insertBefore(style, target.firstChild);
		} else if (lastStyleElementInsertedAtTop.nextSibling) {
			target.insertBefore(style, lastStyleElementInsertedAtTop.nextSibling);
		} else {
			target.appendChild(style);
		}
		stylesInsertedAtTop.push(style);
	} else if (options.insertAt === "bottom") {
		target.appendChild(style);
	} else if (typeof options.insertAt === "object" && options.insertAt.before) {
		var nextSibling = getElement(options.insertAt.before, target);
		target.insertBefore(style, nextSibling);
	} else {
		throw new Error("[Style Loader]\n\n Invalid value for parameter 'insertAt' ('options.insertAt') found.\n Must be 'top', 'bottom', or Object.\n (https://github.com/webpack-contrib/style-loader#insertat)\n");
	}
}

function removeStyleElement (style) {
	if (style.parentNode === null) return false;
	style.parentNode.removeChild(style);

	var idx = stylesInsertedAtTop.indexOf(style);
	if(idx >= 0) {
		stylesInsertedAtTop.splice(idx, 1);
	}
}

function createStyleElement (options) {
	var style = document.createElement("style");

	if(options.attrs.type === undefined) {
		options.attrs.type = "text/css";
	}

	if(options.attrs.nonce === undefined) {
		var nonce = getNonce();
		if (nonce) {
			options.attrs.nonce = nonce;
		}
	}

	addAttrs(style, options.attrs);
	insertStyleElement(options, style);

	return style;
}

function createLinkElement (options) {
	var link = document.createElement("link");

	if(options.attrs.type === undefined) {
		options.attrs.type = "text/css";
	}
	options.attrs.rel = "stylesheet";

	addAttrs(link, options.attrs);
	insertStyleElement(options, link);

	return link;
}

function addAttrs (el, attrs) {
	Object.keys(attrs).forEach(function (key) {
		el.setAttribute(key, attrs[key]);
	});
}

function getNonce() {
	if (false) {}

	return __webpack_require__.nc;
}

function addStyle (obj, options) {
	var style, update, remove, result;

	// If a transform function was defined, run it on the css
	if (options.transform && obj.css) {
	    result = typeof options.transform === 'function'
		 ? options.transform(obj.css) 
		 : options.transform.default(obj.css);

	    if (result) {
	    	// If transform returns a value, use that instead of the original css.
	    	// This allows running runtime transformations on the css.
	    	obj.css = result;
	    } else {
	    	// If the transform function returns a falsy value, don't add this css.
	    	// This allows conditional loading of css
	    	return function() {
	    		// noop
	    	};
	    }
	}

	if (options.singleton) {
		var styleIndex = singletonCounter++;

		style = singleton || (singleton = createStyleElement(options));

		update = applyToSingletonTag.bind(null, style, styleIndex, false);
		remove = applyToSingletonTag.bind(null, style, styleIndex, true);

	} else if (
		obj.sourceMap &&
		typeof URL === "function" &&
		typeof URL.createObjectURL === "function" &&
		typeof URL.revokeObjectURL === "function" &&
		typeof Blob === "function" &&
		typeof btoa === "function"
	) {
		style = createLinkElement(options);
		update = updateLink.bind(null, style, options);
		remove = function () {
			removeStyleElement(style);

			if(style.href) URL.revokeObjectURL(style.href);
		};
	} else {
		style = createStyleElement(options);
		update = applyToTag.bind(null, style);
		remove = function () {
			removeStyleElement(style);
		};
	}

	update(obj);

	return function updateStyle (newObj) {
		if (newObj) {
			if (
				newObj.css === obj.css &&
				newObj.media === obj.media &&
				newObj.sourceMap === obj.sourceMap
			) {
				return;
			}

			update(obj = newObj);
		} else {
			remove();
		}
	};
}

var replaceText = (function () {
	var textStore = [];

	return function (index, replacement) {
		textStore[index] = replacement;

		return textStore.filter(Boolean).join('\n');
	};
})();

function applyToSingletonTag (style, index, remove, obj) {
	var css = remove ? "" : obj.css;

	if (style.styleSheet) {
		style.styleSheet.cssText = replaceText(index, css);
	} else {
		var cssNode = document.createTextNode(css);
		var childNodes = style.childNodes;

		if (childNodes[index]) style.removeChild(childNodes[index]);

		if (childNodes.length) {
			style.insertBefore(cssNode, childNodes[index]);
		} else {
			style.appendChild(cssNode);
		}
	}
}

function applyToTag (style, obj) {
	var css = obj.css;
	var media = obj.media;

	if(media) {
		style.setAttribute("media", media)
	}

	if(style.styleSheet) {
		style.styleSheet.cssText = css;
	} else {
		while(style.firstChild) {
			style.removeChild(style.firstChild);
		}

		style.appendChild(document.createTextNode(css));
	}
}

function updateLink (link, options, obj) {
	var css = obj.css;
	var sourceMap = obj.sourceMap;

	/*
		If convertToAbsoluteUrls isn't defined, but sourcemaps are enabled
		and there is no publicPath defined then lets turn convertToAbsoluteUrls
		on by default.  Otherwise default to the convertToAbsoluteUrls option
		directly
	*/
	var autoFixUrls = options.convertToAbsoluteUrls === undefined && sourceMap;

	if (options.convertToAbsoluteUrls || autoFixUrls) {
		css = fixUrls(css);
	}

	if (sourceMap) {
		// http://stackoverflow.com/a/26603875
		css += "\n/*# sourceMappingURL=data:application/json;base64," + btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))) + " */";
	}

	var blob = new Blob([css], { type: "text/css" });

	var oldSrc = link.href;

	link.href = URL.createObjectURL(blob);

	if(oldSrc) URL.revokeObjectURL(oldSrc);
}


/***/ }),

/***/ "./node_modules/style-loader/lib/urls.js":
/*!***********************************************!*\
  !*** ./node_modules/style-loader/lib/urls.js ***!
  \***********************************************/
/*! no static exports found */
/***/ (function(module, exports) {


/**
 * When source maps are enabled, `style-loader` uses a link element with a data-uri to
 * embed the css on the page. This breaks all relative urls because now they are relative to a
 * bundle instead of the current page.
 *
 * One solution is to only use full urls, but that may be impossible.
 *
 * Instead, this function "fixes" the relative urls to be absolute according to the current page location.
 *
 * A rudimentary test suite is located at `test/fixUrls.js` and can be run via the `npm test` command.
 *
 */

module.exports = function (css) {
  // get current location
  var location = typeof window !== "undefined" && window.location;

  if (!location) {
    throw new Error("fixUrls requires window.location");
  }

	// blank or null?
	if (!css || typeof css !== "string") {
	  return css;
  }

  var baseUrl = location.protocol + "//" + location.host;
  var currentDir = baseUrl + location.pathname.replace(/\/[^\/]*$/, "/");

	// convert each url(...)
	/*
	This regular expression is just a way to recursively match brackets within
	a string.

	 /url\s*\(  = Match on the word "url" with any whitespace after it and then a parens
	   (  = Start a capturing group
	     (?:  = Start a non-capturing group
	         [^)(]  = Match anything that isn't a parentheses
	         |  = OR
	         \(  = Match a start parentheses
	             (?:  = Start another non-capturing groups
	                 [^)(]+  = Match anything that isn't a parentheses
	                 |  = OR
	                 \(  = Match a start parentheses
	                     [^)(]*  = Match anything that isn't a parentheses
	                 \)  = Match a end parentheses
	             )  = End Group
              *\) = Match anything and then a close parens
          )  = Close non-capturing group
          *  = Match anything
       )  = Close capturing group
	 \)  = Match a close parens

	 /gi  = Get all matches, not the first.  Be case insensitive.
	 */
	var fixedCss = css.replace(/url\s*\(((?:[^)(]|\((?:[^)(]+|\([^)(]*\))*\))*)\)/gi, function(fullMatch, origUrl) {
		// strip quotes (if they exist)
		var unquotedOrigUrl = origUrl
			.trim()
			.replace(/^"(.*)"$/, function(o, $1){ return $1; })
			.replace(/^'(.*)'$/, function(o, $1){ return $1; });

		// already a full url? no change
		if (/^(#|data:|http:\/\/|https:\/\/|file:\/\/\/|\s*$)/i.test(unquotedOrigUrl)) {
		  return fullMatch;
		}

		// convert the url to a full url
		var newUrl;

		if (unquotedOrigUrl.indexOf("//") === 0) {
		  	//TODO: should we add protocol?
			newUrl = unquotedOrigUrl;
		} else if (unquotedOrigUrl.indexOf("/") === 0) {
			// path should be relative to the base url
			newUrl = baseUrl + unquotedOrigUrl; // already starts with '/'
		} else {
			// path should be relative to current directory
			newUrl = currentDir + unquotedOrigUrl.replace(/^\.\//, ""); // Strip leading './'
		}

		// send back the fixed url(...)
		return "url(" + JSON.stringify(newUrl) + ")";
	});

	// send back the fixed css
	return fixedCss;
};


/***/ }),

/***/ "./src/app/app-routing.module.ts":
/*!***************************************!*\
  !*** ./src/app/app-routing.module.ts ***!
  \***************************************/
/*! exports provided: AppRoutingModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppRoutingModule", function() { return AppRoutingModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_router__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/router */ "./node_modules/@angular/router/fesm2015/router.js");



const routes = [];
let AppRoutingModule = class AppRoutingModule {
};
AppRoutingModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        imports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"].forRoot(routes)],
        exports: [_angular_router__WEBPACK_IMPORTED_MODULE_2__["RouterModule"]]
    })
], AppRoutingModule);



/***/ }),

/***/ "./src/app/app.component.css":
/*!***********************************!*\
  !*** ./src/app/app.component.css ***!
  \***********************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IiIsImZpbGUiOiJzcmMvYXBwL2FwcC5jb21wb25lbnQuY3NzIn0= */"

/***/ }),

/***/ "./src/app/app.component.ts":
/*!**********************************!*\
  !*** ./src/app/app.component.ts ***!
  \**********************************/
/*! exports provided: AppComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppComponent", function() { return AppComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _node_modules_leaflet_routing_machine_dist_leaflet_routing_machine_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../node_modules/leaflet-routing-machine/dist/leaflet-routing-machine.js */ "./node_modules/leaflet-routing-machine/dist/leaflet-routing-machine.js");
/* harmony import */ var _node_modules_leaflet_routing_machine_dist_leaflet_routing_machine_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_node_modules_leaflet_routing_machine_dist_leaflet_routing_machine_js__WEBPACK_IMPORTED_MODULE_2__);



let AppComponent = class AppComponent {
    constructor() {
        this.title = 'wildfires-frontend';
    }
};
AppComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-root',
        template: __webpack_require__(/*! raw-loader!./app.component.html */ "./node_modules/raw-loader/index.js!./src/app/app.component.html"),
        styles: [__webpack_require__(/*! ./app.component.css */ "./src/app/app.component.css")]
    })
], AppComponent);



/***/ }),

/***/ "./src/app/app.module.ts":
/*!*******************************!*\
  !*** ./src/app/app.module.ts ***!
  \*******************************/
/*! exports provided: AppModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "AppModule", function() { return AppModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_platform_browser__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/platform-browser */ "./node_modules/@angular/platform-browser/fesm2015/platform-browser.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _app_routing_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./app-routing.module */ "./src/app/app-routing.module.ts");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");
/* harmony import */ var _map_map_module__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./map/map.module */ "./src/app/map/map.module.ts");
/* harmony import */ var _app_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./app.component */ "./src/app/app.component.ts");
/* harmony import */ var _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @angular/platform-browser/animations */ "./node_modules/@angular/platform-browser/fesm2015/animations.js");








let AppModule = class AppModule {
};
AppModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_2__["NgModule"])({
        declarations: [
            _app_component__WEBPACK_IMPORTED_MODULE_6__["AppComponent"],
        ],
        imports: [
            _angular_platform_browser__WEBPACK_IMPORTED_MODULE_1__["BrowserModule"],
            _app_routing_module__WEBPACK_IMPORTED_MODULE_3__["AppRoutingModule"],
            _map_map_module__WEBPACK_IMPORTED_MODULE_5__["MapModule"],
            _angular_common_http__WEBPACK_IMPORTED_MODULE_4__["HttpClientModule"],
            _angular_platform_browser_animations__WEBPACK_IMPORTED_MODULE_7__["BrowserAnimationsModule"]
        ],
        providers: [],
        bootstrap: [_app_component__WEBPACK_IMPORTED_MODULE_6__["AppComponent"]]
    })
], AppModule);



/***/ }),

/***/ "./src/app/map/heatmap/heatmap.component.css":
/*!***************************************************!*\
  !*** ./src/app/map/heatmap/heatmap.component.css ***!
  \***************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "#map {\n    height: 100%;\n}\n\n@-webkit-keyframes fly {\n    0% {\n        margin-left: -100px;\n        margin-top: -100px;\n    }\n\n    100% {\n        margin-left: 0;\n        margin-top: 0;\n    }\n}\n\n@keyframes fly {\n    0% {\n        margin-left: -100px;\n        margin-top: -100px;\n    }\n\n    100% {\n        margin-left: 0;\n        margin-top: 0;\n    }\n}\n\n/*For the popup box of tweets in points map*/\n\n.tweet {\n    padding: 8px 8px 4px 8px;\n    font-size: 12px;\n}\n\n.tweet-top {\n    display: flex;\n}\n\n.tweet-user-photo {\n    flex-shrink: 0;\n    background-size: 32px 32px;\n    width: 32px;\n    height: 32px;\n    overflow: hidden;\n    background: #e2e2e2 no-repeat;\n}\n\n.tweet-user-photo img {\n    display: none;\n}\n\n.tweet-body {\n    padding-left: 8px;\n    line-height: 1.2;\n    padding-bottom: 6px;\n}\n\n.tweet-body .name {\n    font-weight: bold;\n    color: #3b94d9;\n    cursor: pointer;\n}\n\n.tweet-body .name:hover {\n    color: #9266CC;\n}\n\n.tweet-body .time {\n    color: #a7a7a7;\n    font-size: 11px;\n}\n\n.tweet-body .user-info {\n    margin-bottom: 2px;\n}\n\n.tweet-media img {\n    width: 100%;\n}\n\n.tweet-link {\n    text-decoration: none;\n    color: #3b94d9;\n}\n\n.tweet-link:hover {\n    text-decoration: underline;\n}\n\n/* button for hiding and showing the timebar */\n\n.slide-up-down {\n    position: absolute;\n    display: inline-block;\n    width: 53px;\n    height: 35px;\n    bottom: 110px;\n    margin-left: 5px;\n}\n\n/*For the popup box of click box*/\n\n.leaflet-popup-content {\n    width: 240px;\n}\n\n.tabs {\n    position: relative;\n    min-height: 200px;\n    clear: both;\n    margin: 25px 0;\n}\n\n.tab {\n    float: left;\n    display: none;\n}\n\n.tab:first-of-type {\n    display: inline-block;\n}\n\n.tabs-link {\n    position: relative;\n    top: -14px;\n    height: 20px;\n    left: -40px;\n}\n\n.tab-link {\n    background: #eee;\n    display: inline-block;\n    padding: 10px;\n    border: 1px solid #ccc;\n    margin-left: -1px;\n    position: relative;\n    list-style-type: none;\n    left: 1px;\n    top: 1px;\n    cursor: pointer;\n}\n\n.tab-link {\n    background: #f8f8f8;\n}\n\n.content {\n    background: white;\n    position: absolute;\n    top: 28px;\n    left: 0;\n    right: 0;\n    bottom: 0;\n    padding: 20px;\n    border: 1px solid #ccc;\n}\n\n.tab:target {\n    display: block;\n}\n\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvbWFwL2hlYXRtYXAvaGVhdG1hcC5jb21wb25lbnQuY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0lBQ0ksWUFBWTtBQUNoQjs7QUFFQTtJQUNJO1FBQ0ksbUJBQW1CO1FBQ25CLGtCQUFrQjtJQUN0Qjs7SUFFQTtRQUNJLGNBQWM7UUFDZCxhQUFhO0lBQ2pCO0FBQ0o7O0FBVkE7SUFDSTtRQUNJLG1CQUFtQjtRQUNuQixrQkFBa0I7SUFDdEI7O0lBRUE7UUFDSSxjQUFjO1FBQ2QsYUFBYTtJQUNqQjtBQUNKOztBQUVBLDRDQUE0Qzs7QUFDNUM7SUFDSSx3QkFBd0I7SUFDeEIsZUFBZTtBQUNuQjs7QUFFQTtJQUVJLGFBQWE7QUFDakI7O0FBRUE7SUFFSSxjQUFjO0lBQ2QsMEJBQTBCO0lBQzFCLFdBQVc7SUFDWCxZQUFZO0lBQ1osZ0JBQWdCO0lBQ2hCLDZCQUE2QjtBQUNqQzs7QUFFQTtJQUNJLGFBQWE7QUFDakI7O0FBRUE7SUFDSSxpQkFBaUI7SUFDakIsZ0JBQWdCO0lBQ2hCLG1CQUFtQjtBQUN2Qjs7QUFFQTtJQUNJLGlCQUFpQjtJQUNqQixjQUFjO0lBQ2QsZUFBZTtBQUNuQjs7QUFFQTtJQUNJLGNBQWM7QUFDbEI7O0FBRUE7SUFDSSxjQUFjO0lBQ2QsZUFBZTtBQUNuQjs7QUFFQTtJQUNJLGtCQUFrQjtBQUN0Qjs7QUFFQTtJQUNJLFdBQVc7QUFDZjs7QUFFQTtJQUNJLHFCQUFxQjtJQUNyQixjQUFjO0FBQ2xCOztBQUVBO0lBQ0ksMEJBQTBCO0FBQzlCOztBQUVBLDhDQUE4Qzs7QUFDOUM7SUFDSSxrQkFBa0I7SUFDbEIscUJBQXFCO0lBQ3JCLFdBQVc7SUFDWCxZQUFZO0lBQ1osYUFBYTtJQUNiLGdCQUFnQjtBQUNwQjs7QUFHQSxpQ0FBaUM7O0FBQ2pDO0lBQ0ksWUFBWTtBQUNoQjs7QUFFQTtJQUNJLGtCQUFrQjtJQUNsQixpQkFBaUI7SUFDakIsV0FBVztJQUNYLGNBQWM7QUFDbEI7O0FBRUE7SUFDSSxXQUFXO0lBQ1gsYUFBYTtBQUNqQjs7QUFFQTtJQUNJLHFCQUFxQjtBQUN6Qjs7QUFFQTtJQUNJLGtCQUFrQjtJQUNsQixVQUFVO0lBQ1YsWUFBWTtJQUNaLFdBQVc7QUFDZjs7QUFFQTtJQUNJLGdCQUFnQjtJQUNoQixxQkFBcUI7SUFDckIsYUFBYTtJQUNiLHNCQUFzQjtJQUN0QixpQkFBaUI7SUFDakIsa0JBQWtCO0lBQ2xCLHFCQUFxQjtJQUNyQixTQUFTO0lBQ1QsUUFBUTtJQUNSLGVBQWU7QUFDbkI7O0FBRUE7SUFDSSxtQkFBbUI7QUFDdkI7O0FBRUE7SUFDSSxpQkFBaUI7SUFDakIsa0JBQWtCO0lBQ2xCLFNBQVM7SUFDVCxPQUFPO0lBQ1AsUUFBUTtJQUNSLFNBQVM7SUFDVCxhQUFhO0lBQ2Isc0JBQXNCO0FBQzFCOztBQUVBO0lBQ0ksY0FBYztBQUNsQiIsImZpbGUiOiJzcmMvYXBwL21hcC9oZWF0bWFwL2hlYXRtYXAuY29tcG9uZW50LmNzcyIsInNvdXJjZXNDb250ZW50IjpbIiNtYXAge1xuICAgIGhlaWdodDogMTAwJTtcbn1cblxuQGtleWZyYW1lcyBmbHkge1xuICAgIDAlIHtcbiAgICAgICAgbWFyZ2luLWxlZnQ6IC0xMDBweDtcbiAgICAgICAgbWFyZ2luLXRvcDogLTEwMHB4O1xuICAgIH1cblxuICAgIDEwMCUge1xuICAgICAgICBtYXJnaW4tbGVmdDogMDtcbiAgICAgICAgbWFyZ2luLXRvcDogMDtcbiAgICB9XG59XG5cbi8qRm9yIHRoZSBwb3B1cCBib3ggb2YgdHdlZXRzIGluIHBvaW50cyBtYXAqL1xuLnR3ZWV0IHtcbiAgICBwYWRkaW5nOiA4cHggOHB4IDRweCA4cHg7XG4gICAgZm9udC1zaXplOiAxMnB4O1xufVxuXG4udHdlZXQtdG9wIHtcbiAgICBkaXNwbGF5OiAtbXMtZmxleGJveDtcbiAgICBkaXNwbGF5OiBmbGV4O1xufVxuXG4udHdlZXQtdXNlci1waG90byB7XG4gICAgLW1zLWZsZXgtbmVnYXRpdmU6IDA7XG4gICAgZmxleC1zaHJpbms6IDA7XG4gICAgYmFja2dyb3VuZC1zaXplOiAzMnB4IDMycHg7XG4gICAgd2lkdGg6IDMycHg7XG4gICAgaGVpZ2h0OiAzMnB4O1xuICAgIG92ZXJmbG93OiBoaWRkZW47XG4gICAgYmFja2dyb3VuZDogI2UyZTJlMiBuby1yZXBlYXQ7XG59XG5cbi50d2VldC11c2VyLXBob3RvIGltZyB7XG4gICAgZGlzcGxheTogbm9uZTtcbn1cblxuLnR3ZWV0LWJvZHkge1xuICAgIHBhZGRpbmctbGVmdDogOHB4O1xuICAgIGxpbmUtaGVpZ2h0OiAxLjI7XG4gICAgcGFkZGluZy1ib3R0b206IDZweDtcbn1cblxuLnR3ZWV0LWJvZHkgLm5hbWUge1xuICAgIGZvbnQtd2VpZ2h0OiBib2xkO1xuICAgIGNvbG9yOiAjM2I5NGQ5O1xuICAgIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuLnR3ZWV0LWJvZHkgLm5hbWU6aG92ZXIge1xuICAgIGNvbG9yOiAjOTI2NkNDO1xufVxuXG4udHdlZXQtYm9keSAudGltZSB7XG4gICAgY29sb3I6ICNhN2E3YTc7XG4gICAgZm9udC1zaXplOiAxMXB4O1xufVxuXG4udHdlZXQtYm9keSAudXNlci1pbmZvIHtcbiAgICBtYXJnaW4tYm90dG9tOiAycHg7XG59XG5cbi50d2VldC1tZWRpYSBpbWcge1xuICAgIHdpZHRoOiAxMDAlO1xufVxuXG4udHdlZXQtbGluayB7XG4gICAgdGV4dC1kZWNvcmF0aW9uOiBub25lO1xuICAgIGNvbG9yOiAjM2I5NGQ5O1xufVxuXG4udHdlZXQtbGluazpob3ZlciB7XG4gICAgdGV4dC1kZWNvcmF0aW9uOiB1bmRlcmxpbmU7XG59XG5cbi8qIGJ1dHRvbiBmb3IgaGlkaW5nIGFuZCBzaG93aW5nIHRoZSB0aW1lYmFyICovXG4uc2xpZGUtdXAtZG93biB7XG4gICAgcG9zaXRpb246IGFic29sdXRlO1xuICAgIGRpc3BsYXk6IGlubGluZS1ibG9jaztcbiAgICB3aWR0aDogNTNweDtcbiAgICBoZWlnaHQ6IDM1cHg7XG4gICAgYm90dG9tOiAxMTBweDtcbiAgICBtYXJnaW4tbGVmdDogNXB4O1xufVxuXG5cbi8qRm9yIHRoZSBwb3B1cCBib3ggb2YgY2xpY2sgYm94Ki9cbi5sZWFmbGV0LXBvcHVwLWNvbnRlbnQge1xuICAgIHdpZHRoOiAyNDBweDtcbn1cblxuLnRhYnMge1xuICAgIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgICBtaW4taGVpZ2h0OiAyMDBweDtcbiAgICBjbGVhcjogYm90aDtcbiAgICBtYXJnaW46IDI1cHggMDtcbn1cblxuLnRhYiB7XG4gICAgZmxvYXQ6IGxlZnQ7XG4gICAgZGlzcGxheTogbm9uZTtcbn1cblxuLnRhYjpmaXJzdC1vZi10eXBlIHtcbiAgICBkaXNwbGF5OiBpbmxpbmUtYmxvY2s7XG59XG5cbi50YWJzLWxpbmsge1xuICAgIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgICB0b3A6IC0xNHB4O1xuICAgIGhlaWdodDogMjBweDtcbiAgICBsZWZ0OiAtNDBweDtcbn1cblxuLnRhYi1saW5rIHtcbiAgICBiYWNrZ3JvdW5kOiAjZWVlO1xuICAgIGRpc3BsYXk6IGlubGluZS1ibG9jaztcbiAgICBwYWRkaW5nOiAxMHB4O1xuICAgIGJvcmRlcjogMXB4IHNvbGlkICNjY2M7XG4gICAgbWFyZ2luLWxlZnQ6IC0xcHg7XG4gICAgcG9zaXRpb246IHJlbGF0aXZlO1xuICAgIGxpc3Qtc3R5bGUtdHlwZTogbm9uZTtcbiAgICBsZWZ0OiAxcHg7XG4gICAgdG9wOiAxcHg7XG4gICAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG4udGFiLWxpbmsge1xuICAgIGJhY2tncm91bmQ6ICNmOGY4Zjg7XG59XG5cbi5jb250ZW50IHtcbiAgICBiYWNrZ3JvdW5kOiB3aGl0ZTtcbiAgICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gICAgdG9wOiAyOHB4O1xuICAgIGxlZnQ6IDA7XG4gICAgcmlnaHQ6IDA7XG4gICAgYm90dG9tOiAwO1xuICAgIHBhZGRpbmc6IDIwcHg7XG4gICAgYm9yZGVyOiAxcHggc29saWQgI2NjYztcbn1cblxuLnRhYjp0YXJnZXQge1xuICAgIGRpc3BsYXk6IGJsb2NrO1xufVxuIl19 */"

/***/ }),

/***/ "./src/app/map/heatmap/heatmap.component.ts":
/*!**************************************************!*\
  !*** ./src/app/map/heatmap/heatmap.component.ts ***!
  \**************************************************/
/*! exports provided: HeatmapComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "HeatmapComponent", function() { return HeatmapComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var leaflet_heatmap_leaflet_heatmap_js__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! leaflet-heatmap/leaflet-heatmap.js */ "./node_modules/leaflet-heatmap/leaflet-heatmap.js");
/* harmony import */ var leaflet_heatmap_leaflet_heatmap_js__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(leaflet_heatmap_leaflet_heatmap_js__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../services/map-service/map.service */ "./src/app/services/map-service/map.service.ts");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! leaflet-maskcanvas */ "./node_modules/leaflet-maskcanvas/dist/L.GridLayer.MaskCanvas.js");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! leaflet-velocity-ts */ "./node_modules/leaflet-velocity-ts/dist/leaflet-velocity.js");
/* harmony import */ var leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var highcharts__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! highcharts */ "./node_modules/highcharts/highcharts.js");
/* harmony import */ var highcharts__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(highcharts__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _services_search_search_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../services/search/search.service */ "./src/app/services/search/search.service.ts");
/* harmony import */ var _services_fire_service_fire_service__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ../../services/fire-service/fire.service */ "./src/app/services/fire-service/fire.service.ts");
/* harmony import */ var _layers_fire_tweet_layer__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ../layers/fire.tweet.layer */ "./src/app/map/layers/fire.tweet.layer.ts");
/* harmony import */ var _layers_wind_layer__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ../layers/wind.layer */ "./src/app/map/layers/wind.layer.ts");
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _layers_fire_region_layer__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ../layers/fire.region.layer */ "./src/app/map/layers/fire.region.layer.ts");
/* harmony import */ var _layers_location_boundary_layer__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ../layers/location.boundary.layer */ "./src/app/map/layers/location.boundary.layer.ts");
/* harmony import */ var _layers_location_marker__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! ../layers/location.marker */ "./src/app/map/layers/location.marker.ts");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _services_time_time_service__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! ../../services/time/time.service */ "./src/app/services/time/time.service.ts");
var HeatmapComponent_1;

/**
 * @author Yuan Fu <yuanf9@uci.edu>
 * @author (Hugo) Qiaonan Huang <qiaonanh@uci.edu>
 */
















let HeatmapComponent = HeatmapComponent_1 = class HeatmapComponent {
    constructor(mapService, searchService, fireService, timeService) {
        this.mapService = mapService;
        this.searchService = searchService;
        this.fireService = fireService;
        this.timeService = timeService;
        this.pinRadius = 40000;
        // For what to present when click event happens
        this.marker = null;
        this.timer = null;
        // Set up for a range and each smaller interval of temp to give specific color layers
        this.tempLayers = [];
        this.tempBreaks = [-6, -3, 0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36];
        this.colorList = ['#393fb8', '#45afd6', '#49ebd8', '#49eb8f',
            '#a6e34b', '#f2de5a', '#edbf18', '#e89c20',
            '#f27f02', '#f25a02', '#f23a02', '#f0077f',
            '#f205c3', '#9306ba'
        ];
        // For temp range selector store current max/min selected by user
        this.tempRegionsMax = [];
        this.tempMax = 36;
        this.tempMin = 0;
        // fireEventHandler = (data) => {
        //
        //     const fireEventList = [];
        //
        //     for (const ev of data.fireEvents) {
        //         const point = [ev.lat, ev.long];
        //         const size = 40;
        //         const fireIcon = L.icon({
        //             iconUrl: 'assets/image/pixelfire.gif',
        //             iconSize: [size, size],
        //         });
        //         const marker = L.marker(point, {icon: fireIcon}).bindPopup('I am on fire(image>40%). My evidence is:<br/>' + ev.text);
        //         fireEventList.push(marker);
        //
        //     }
        //     const fireEvents = L.layerGroup(fireEventList);
        //     this.mainControl.addOverlay(fireEvents, 'Fire event');
        // };
        this.heatmapDataHandler = (data) => {
            /**
             *  Display temp data as a heatmap with color scale.
             *
             *  Receive data with geolocation and temp value as points with value;
             *  showed as different color with customized color scale;
             *  use heatmapOverlay class from leaflet-heatmap.
             *
             *  @param {Object} geolocation value and temp value
             *
             *  @link https://www.patrick-wied.at/static/heatmapjs/docs.html#heatmap-setData
             */
            const heatmapConfig = {
                radius: 1,
                maxOpacity: 0.63,
                minOpacity: 0.2,
                scaleRadius: true,
                useLocalExtrema: false,
                blur: 1,
                latField: 'lat',
                lngField: 'long',
                valueField: 'temp',
                // gradient is customized to match the color scales of temp plotting layers exactly the same
                gradient: {
                    '.1': '#393fb8',
                    '.2': '#45afd6',
                    '.3': '#49ebd8',
                    '.4': '#49eb8f',
                    '.5': '#a6e34b',
                    '.55': '#f2de5a',
                    '.6': '#edbf18',
                    '.65': '#e89c20',
                    '.7': '#f27f02',
                    '.75': '#f25a02',
                    '.8': '#f23a02',
                    '.85': '#f0077f',
                    '.9': '#f205c3',
                    '.99': '#9306ba',
                }
            };
            const heatmapLayer = new leaflet_heatmap_leaflet_heatmap_js__WEBPACK_IMPORTED_MODULE_2___default.a(heatmapConfig);
            // 'max' should be far higher than the upper domain of data, to make the color distinguish each different data
            heatmapLayer.setData({ max: 680, data });
            this.mainControl.addOverlay(heatmapLayer, 'Temp heatmap');
        };
        this.dotMapDataHandler = (data) => {
            /**
             *  Assign 14 different color layers for all temp data.
             *
             *  Classify points for different temp into different list
             *  Assign a different color and a layer for each small temperature interval, and push these layer
             *
             *  @param {Object} geolocation value and temp value
             */
            const latLongBins = [];
            // Classify points for different temp into different list
            for (let t = 0; t < this.tempBreaks.length - 1; t++) {
                const points = [];
                for (const point of data) {
                    if (point.temp >= this.tempBreaks[t] && point.temp <= this.tempBreaks[t + 1]) { // one list for one small temp interval
                        points.push([Number(point.lat), Number(point.long)]);
                    }
                }
                latLongBins.push(points);
            }
            // Assign different color for each temperature interval
            for (let i = 0; i < this.colorList.length; i++) {
                this.tempLayer = L.TileLayer.maskCanvas({
                    radius: 5,
                    useAbsoluteRadius: true,
                    color: '#000',
                    opacity: 0.85,
                    noMask: true,
                    lineColor: this.colorList[i]
                });
                this.tempLayer.setData(latLongBins[i]);
                this.tempLayers.push(this.tempLayer);
            }
        };
        this.clickPointHandler = (data) => {
            /**
             *  Handle the aggregated data got from backend and display as charts
             *
             *  First, convert data to fit drawchart function
             *  Also, deal with null values
             *  Then, second popup generated, 3 charts indicating Moisture, Temperature, Precipitation within that clickbox circle
             *
             *  @param 3 lists of environmental data (Moisture, Temperature, Precipitation) with time, and value
             */
            // convert data to fit drawchart function
            // deal with null values
            const cntTime = [];
            const cntValue = [];
            for (const tweetcnt of data.cnt_tweet) {
                cntTime.push(tweetcnt[0]);
                if (tweetcnt[1] === null) {
                    cntValue.push(0);
                }
                else {
                    cntValue.push(tweetcnt[1]);
                }
            }
            const tmpTime = [];
            const tmpValue = [];
            for (const avgtmp of data.tmp) {
                tmpTime.push(avgtmp[0]);
                if (avgtmp[1] === null) {
                    tmpValue.push(0);
                }
                else {
                    tmpValue.push(avgtmp[1]); // PRISM data: unit Celsius
                }
            }
            const soilwTime = [];
            const soilwValue = [];
            for (const avgsoilw of data.soilw) {
                soilwTime.push(avgsoilw[0]);
                if (avgsoilw[1] === null) {
                    soilwValue.push(0);
                }
                else {
                    soilwValue.push(avgsoilw[1]); // PRISM data: unit %
                }
            }
            const pptTime = [];
            const pptValue = [];
            for (const avgppt of data.ppt) {
                pptTime.push(avgppt[0]);
                if (avgppt[1] === null) {
                    pptValue.push(0);
                }
                else {
                    pptValue.push(avgppt[1]);
                }
            }
            // Second popup generated, 3 charts indicating Moisture, Temperature, Precipitation within that clickbox circle
            this.marker.bindPopup(this.clickboxContentsToShow).openPopup();
            HeatmapComponent_1.drawChart('container', soilwTime, 'Tweet counts', cntValue, 'tweets', 'Moisture', soilwValue, '%', '#d9db9c');
            HeatmapComponent_1.drawChart('container2', tmpTime, 'Tweet counts', cntValue, 'tweets', 'Temperature', tmpValue, 'Celsius', '#c4968b');
            HeatmapComponent_1.drawChart('container3', pptTime, 'Tweet counts', cntValue, 'tweets', 'Precipitation', pptValue, 'mm', '#9fc7c3');
            // if popup closed, remove the whole clickbox
            this.marker.getPopup().on('remove', () => {
                this.group.remove();
            });
            // if (this.marker.isSticky) {
            //     this.group.addTo(this.map);
            // }
        };
        // TODO: Add Sticky botton for clickbox later
        // stickyBotton = () => {
        //     const clickboxContents = $('<div />');
        //     clickboxContents.html('<button href="#" class="leaflet-popup-sticky-button1">S</button><br>')
        //         .on('click', '.leaflet-popup-sticky-button1', () => {
        //             this.marker.isSticky = !this.marker.isSticky;
        //             if (this.marker.isSticky) {
        //                 this.group.addTo(this.map);
        //             }
        //         });
        //     clickboxContents.append(this.clickboxContentsToShow);
        //     return clickboxContents[0];
        // };
        this.rangeSelectHandler = (event) => {
            /**
             *  Add dotmap layers satisfy the temp range user selected
             *
             *  Respond to the input range of temperature from the range selector in side bar;
             *  used a varint to always keep the latest input Max/Min temperature;
             *  pushed layers in selected range into list tempRegionsMax;
             *  added new canvas layers in the updated list tempRegionsMax to Map
             *
             *  @param {Object} a list with current lower and upper temp bound that user gives
             */
            const inRange = (min, max, target) => {
                return target < max && target >= min;
            };
            // Respond to the input range of temperature from the range selector in side bar
            // var int: always keep the latest input Max/Min temperature
            if (event.high !== undefined) {
                this.tempMax = event.high;
            }
            if (event.low !== undefined) {
                this.tempMin = event.low;
            }
            if (this.tempMin <= this.tempMax) {
                this.tempRegionsMax = [];
                let startSelecting = false;
                // Push layers in selected range into list tempRegionsMax
                for (let i = 0; i < this.tempBreaks.length - 1; i++) {
                    const rangeMin = this.tempBreaks[i];
                    const rangeMax = this.tempBreaks[i + 1];
                    if (inRange(rangeMin, rangeMax, this.tempMin)) {
                        startSelecting = true;
                    }
                    if (startSelecting) {
                        this.tempRegionsMax.push(this.tempLayers[i]);
                    }
                    if (inRange(rangeMin, rangeMax, this.tempMax)) {
                        startSelecting = false;
                        break;
                    }
                }
                // Remove previous canvas layers
                for (const layer of this.tempLayers) {
                    this.map.removeLayer(layer);
                }
                // Add new canvas layers in the updated list tempRegionsMax to Map
                for (const region of this.tempRegionsMax) {
                    region.addTo(this.map);
                }
            }
        };
        this.boundaryDataHandler = ([[data], value]) => {
            // given the boundary data after the keyword search, fits the map according to the boundary and shows the name label
            // not plotting anything, only zooming in
            const listWithFixedLL = [];
            if (data) {
                // list will be converted because of the lat and lon are misplaced
                for (const item of data.coordinates[0]) {
                    listWithFixedLL.push([parseFloat(item[1]), parseFloat(item[0])]);
                }
                this.map.fitBounds(listWithFixedLL); // fits map according to the given fixed boundary list
                const centerLatLng = this.getPolygonCenter(listWithFixedLL);
                this.mapService.searchMarkerLoaded.emit([centerLatLng, value]);
                // sends the center of the polygon to the location.boundary layer
            }
        };
        this.getPolygonCenter = (coordinateArr) => {
            // gets the center point when given a coordinate array
            // OPTIMIZE: the get polygon center function
            const x = coordinateArr.map(a => a[0]);
            const y = coordinateArr.map(a => a[1]);
            const minX = Math.min.apply(null, x);
            const maxX = Math.max.apply(null, x);
            const minY = Math.min.apply(null, y);
            const maxY = Math.max.apply(null, y);
            return [(minX + maxX) / 2, (minY + maxY) / 2];
        };
    }
    static drawChart(name, xValue, y1Name, y1Value, y1Unit, y2Name, y2Value, y2Unit, y2Color) {
        /**
         *  Static format for popup chart content
         *
         *  Define format of the highcharts in clickbox, Each chart has 2 y axises for 2 plots : y1, y2
         *  y1 color is set static, y2 color takes as a parameter
         *
         *  @param {Type} inputs including name,list of value, and units for each plots
         */
        highcharts__WEBPACK_IMPORTED_MODULE_6__["chart"](name, {
            title: {
                text: '',
            },
            chart: {
                zoomType: 'x',
                style: {
                    fontSize: '10px',
                },
            },
            xAxis: {
                categories: xValue,
                crosshair: true,
            },
            plotOptions: {
                series: {
                    allowPointSelect: true,
                }
            },
            yAxis: [{
                    labels: {
                        format: '{value}' + y1Unit,
                        style: {
                            color: '#3b2f31',
                            fontSize: '8px',
                        }
                    },
                    title: {
                        text: '',
                    }
                }, {
                    title: {
                        text: '',
                    },
                    labels: {
                        format: '{value} ' + y2Unit,
                        style: {
                            color: y2Color,
                            fontSize: '8px',
                        }
                    },
                    opposite: true
                }],
            tooltip: {
                shared: true,
            },
            series: [{
                    name: y2Name,
                    type: 'spline',
                    color: y2Color,
                    yAxis: 1,
                    data: y2Value,
                    tooltip: {
                        valueSuffix: ' ' + y2Unit,
                    },
                    showInLegend: false
                }, {
                    name: y1Name,
                    type: 'spline',
                    color: '#3b2f31',
                    data: y1Value,
                    yAxis: 0,
                    tooltip: {
                        valueSuffix: y1Unit,
                    },
                    showInLegend: false
                }]
        });
    }
    ngOnInit() {
        // Initialize map and 3 base layers
        const mapBoxUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoibWFwYm94IiwiY' +
            'SI6ImNpejY4NXVycTA2emYycXBndHRqcmZ3N3gifQ.rJcFIG214AriISLbB6B5aw';
        const satellite = L.tileLayer(mapBoxUrl, { id: 'mapbox.satellite' });
        const streets = L.tileLayer(mapBoxUrl, { id: 'mapbox.streets' });
        const dark = L.tileLayer(mapBoxUrl, { id: 'mapbox.dark' });
        this.map = L.map('map', {
            center: [33.64, -117.84],
            zoom: 5,
            maxzoom: 22,
            layers: [satellite, streets, dark]
        });
        // Initialize base layer group
        const baseLayers = {
            '<span style =\'color:blue\'>Satellite</span>': satellite,
            '<span style =\'color:red\'>Streets</span>': streets,
            '<span style =\'color:black\'>Dark</span>': dark
        };
        this.mainControl = L.control.layers(baseLayers).addTo(this.map);
        // Generate coordinate in sidebar
        this.map.addEventListener('mousemove', (ev) => {
            const lat = ev.latlng.lat;
            const lng = ev.latlng.lng;
            jquery__WEBPACK_IMPORTED_MODULE_1__('#mousePosition').html('Lat: ' + Math.round(lat * 100) / 100 + ' Lng: ' + Math.round(lng * 100) / 100);
        });
        // Get temperature data from service
        const tempSubject = new rxjs__WEBPACK_IMPORTED_MODULE_11__["Subject"]();
        tempSubject.subscribe(this.dotMapDataHandler);
        tempSubject.subscribe(this.heatmapDataHandler);
        this.mapService.getTemperatureData().subscribe(tempSubject);
        // Get tweets data from service
        this.fireTweetLayer = new _layers_fire_tweet_layer__WEBPACK_IMPORTED_MODULE_9__["FireTweetLayer"](this.mainControl, this.mapService, this.map, this.timeService);
        // Get fire events data from service
        // this.fireEventLayer = new FireEventLayer(this.mainControl, this.mapService, this.map);
        this.fireRegionLayer = new _layers_fire_region_layer__WEBPACK_IMPORTED_MODULE_12__["FireRegionLayer"](this.mainControl, this.mapService, this.map, this.fireService, this.timeService);
        this.locationBoundaryLayer = new _layers_location_boundary_layer__WEBPACK_IMPORTED_MODULE_13__["LocationBoundaryLayer"](this.mainControl, this.mapService, this.map);
        this.locationMarkerLayer = new _layers_location_marker__WEBPACK_IMPORTED_MODULE_14__["LocationMarkerLayer"](this.mainControl, this.mapService, this.map);
        // Get wind events data from service
        this.windLayer = new _layers_wind_layer__WEBPACK_IMPORTED_MODULE_10__["WindLayer"](this.mainControl, this.mapService);
        // Get boundary data from service to draw it on map
        this.searchService.searchDataLoaded.subscribe(this.boundaryDataHandler);
        // Add event Listener when user specify a time range on time series
        jquery__WEBPACK_IMPORTED_MODULE_1__(window).on('timeRangeChange', this.fireTweetLayer.timeRangeChangeHandler);
        jquery__WEBPACK_IMPORTED_MODULE_1__(window).on('timeRangeChange', this.fireRegionLayer.timeRangeChangeFirePolygonHandler);
        // $(window).on('timeRangeChange', this.fireEventLayer.timeRangeChangeFireEventHandler);
        // Send temp range selected from service
        this.mapService.temperatureChangeEvent.subscribe(this.rangeSelectHandler);
        this.map.on('mousedown', e => this.onMapHold(e));
        this.mapService.getRecentTweetData().subscribe(data => this.fireTweetLayer.recentTweetLoadHandler(data));
    }
    onMapClick(e) {
        /**
         *  The major function to generate pin with a simple popup after click-hold event
         *
         *  Include several sub-functions which would be explained seperately.
         *  Despite separated functions, it generate customize icon marker, also group the circle together
         *  change bound color when mouse on to tell user your mouse is on, with an upper bound of radius
         *  when mousedown, judge if the mouse moved when mouseup, if not moved then this is a common click on map
         *
         *  @param event with geolocation value
         */
        // TODO: Add old clickbox according to Sticky botton
        // const oldMarker = this.marker;
        // const oldGroup = this.group;
        // if (oldMarker !== null) {
        //     if (oldMarker.isSticky) {
        //         oldGroup.addTo(this.map);
        //     }
        // }
        let aggregatedDataSubInBound; // To unsubscribe later
        function mouseMoveChangeRadius(event) {
            /**
             *  To set radius of circle and bound together when the drag event happens
             *
             *  @param event of mouseup with geolocation value
             */
            let newRadius = distance(circle._latlng, event.latlng);
            if (newRadius > 2 * 111000) {
                // Set upper bound of radius of clickbox (2 degree); 2 degree = 2 * 111000 meter
                newRadius = 2 * 111000;
                console.log('Reaches the upper bound of radius (2 degree)');
            }
            localBound.setRadius(newRadius);
            circle.setRadius(newRadius);
        }
        function distance(center, pt) {
            /**
             *  convert unit : degree of latlng to meter. eg: 1degree = 111km = 111000m
             *
             *  @param (center of circle, latlng of current location)
             */
            return 111000 * Math.sqrt(Math.pow(center.lat - pt.lat, 2) + Math.pow(center.lng - pt.lng, 2));
        }
        const clickIcon = L.icon({
            iconUrl: 'assets/image/pin6.gif',
            iconSize: [26, 30],
        });
        const marker = L.marker(e.latlng, { draggable: false, icon: clickIcon });
        // TODO: Add isSticky switch for clickbox
        // marker.isSticky = false;
        const circle = L.circle(e.latlng, {
            stroke: false,
            fillColor: 'white',
            fillOpacity: 0.35,
            radius: 40000,
        });
        const localBound = L.circle(e.latlng, {
            radius: 40000,
            color: 'white',
            weight: 5,
            fill: false,
            bubblingMouseEvents: false,
        })
            // change bound color when mouse on to tell user your mouse is on
            .on('mouseover', () => {
            localBound.setStyle({ color: '#919191' });
        })
            .on('mouseout', () => {
            localBound.setStyle({ color: 'white' });
        })
            .on('mousedown', () => {
            // deal with drag event when mouseon circle bound
            this.map.removeEventListener('click');
            this.map.dragging.disable();
            this.map.on('mousemove', mouseMoveChangeRadius);
            // send changed radius to backend with mousedown/mouseup
            this.map.on('mouseup', (event) => {
                let newRadius = distance(circle._latlng, event.latlng);
                if (newRadius > 2 * 111000) {
                    // upper bound of radius
                    newRadius = 2 * 111000;
                }
                // convert unit :  meter to degree of latlng. eg: 1degree = 111km = 111000m
                aggregatedDataSubInBound = this.mapService.getClickData(e.latlng.lat, e.latlng.lng, newRadius / 111000, new Date(this.timeService.getRangeDate()[1]).toISOString(), 7)
                    .subscribe(this.clickPointHandler);
                this.map.dragging.enable();
                this.map.removeEventListener('mousemove', mouseMoveChangeRadius);
                setTimeout(() => {
                    this.map.on('mousedown', this.onMapHold, this);
                    this.map.removeEventListener('mouseup');
                }, 500);
            }, this);
        });
        // group 3 item as a group, so they can be added or removed together
        const group = L.layerGroup([marker, circle, localBound]).addTo(this.map);
        // First popup generated, with geolocation info
        marker.bindPopup('You clicked the map at ' + e.latlng.toString(), {
            closeOnClick: false,
            autoClose: true,
        }).openPopup();
        // when mousedown, judge if the mouse moved when mouseup, if not moved then this is a common click on map
        // we aimed to remove the whole clickbox when user do a common click
        this.map.on('mousedown', (e) => this.judgeDistance(e, group));
        this.marker = marker;
        this.group = L.layerGroup([marker, circle, localBound]);
        // TODO: change marker from global var since it only specify one.
        const aggregatedDataSub = this.mapService.getClickData(e.latlng.lat, e.latlng.lng, this.pinRadius / 111000, new Date(this.timeService.getRangeDate()[1]).toISOString(), 7)
            .subscribe(this.clickPointHandler);
        // Remove popup fire remove all (default is not sticky)
        marker.getPopup().on('remove', () => {
            group.remove();
            aggregatedDataSub.unsubscribe();
            if (aggregatedDataSubInBound !== undefined) {
                // unsubscribe when backend data was sending but frontend clickbox was closed by user, otherwise backend data has no place to display
                aggregatedDataSubInBound.unsubscribe();
            }
        });
    }
    // TODO: Add Sticky feature for clickbox later
    judgeDistance(event, group) {
        /**
         *  Judge if the mousedown and mouseup as the same coordinate location, if not, then remove clickbox
         *
         *  @param event with geolocation value, and the grouped components: marker, circle, bound
         */
        this.map.on('mouseup', (e) => {
            if (event.latlng.lat === e.latlng.lat && event.latlng.lng === e.latlng.lng) {
                // if (!that.marker.isSticky) {
                group.remove();
                // }
            }
        });
    }
    onMapHold(event) {
        /**
         *  Fire clickbox if mouse down hold for  > 1000ms
         *
         *  @param event with geolocation
         */
        const duration = 1000;
        if (this.timer !== null) {
            clearTimeout(this.timer);
            this.timer = null;
        }
        this.map.on('mouseup', () => {
            clearTimeout(this.timer);
            this.timer = null;
        });
        this.timer = setTimeout(L.Util.bind(() => {
            Object(rxjs__WEBPACK_IMPORTED_MODULE_11__["of"])(event).subscribe((ev) => this.onMapClick(ev));
            this.timer = null;
        }, this), duration);
    }
    clickboxContentsToShow() {
        /**
         *  Format of clickbox with 3 tabs structured
         *
         *  Three Highcharts added under first tab
         */
        // HTML for the 3 highcharts
        const chartContents = '    <div id="containers" style="width: 280px; height: 360px;">\n' +
            '    <div id="container" style="width: 280px; height: 120px; margin: 0px; float: left;"></div>\n' +
            '    <div id="container2" style="width: 280px; height: 120px; margin: 0px; float: left;"></div>\n' +
            '    <div id="container3" style="width: 280px; height: 120px; margin: 0px; float: left;"></div>\n';
        // HTML for the tabs inside clickbox
        // Inside style is CSS content
        const clickboxContents = '<style>' +
            `.leaflet-popup-content {
                width: 400px;
            }
            .tabs {
                position: relative;
                min-height: 400px;
                min-width: 320px;
                clear: both;
                margin: 0px 0;
            }
            .tab {
                float: left;
                display: none;
            }
            .tab:first-of-type {
                display: inline-block;
            }
            .tabs-link {
                position: relative;
                top: -14px;
                height: 20px;
                left: -40px;
            }
            .tab-link {
                background: #eee;
                display: inline-block;
                padding: 10px;
                border: 1px solid #ccc;
                margin-left: -1px;
                position: relative;
                list-style-type: none;
                left: 1px;
                top: 1px;
                cursor: pointer;
            }
            .tab-link {
                background: #f8f8f8;
            }
            .content {
                background: white;
                position: absolute;
                top: 28px;
                left: 0;
                right: 0;
                bottom: 0;
                padding: 20px;
                border: 1px solid #ccc;
            }
            .tab:target {
                display: block;
            }` +
            '</style>' +
            '<div class="tabs" >' +
            '<div class="tab" id="tab-1" >' +
            '<div class="content">' +
            '<b>' +
            chartContents +
            '</b>' +
            '</div>' +
            '</div>' +
            '<div class="tab" id="tab-2" >' +
            '<div class="content">' +
            '<b>Put tweets contents here later</b>' +
            '</div>' +
            '</div>' +
            '<div class="tab" id="tab-3" >' +
            '<div class="content">' +
            '<b>whatever else</b>' +
            '</div>' +
            '</div>' +
            '<ul class="tabs-link">' +
            '<li class="tab-link"> <a href="#tab-1"><span>Charts</span></a></li>' +
            '<li class="tab-link"> <a href="#tab-2"><span>Tweets</span></a></li>' +
            '<li class="tab-link"> <a href="#tab-3"><span>Else</span></a></li>' +
            '</ul>' +
            '</div>';
        return clickboxContents;
    }
};
HeatmapComponent.STATE_LEVEL_ZOOM = 8;
HeatmapComponent.COUNTY_LEVEL_ZOOM = 9;
HeatmapComponent.ctorParameters = () => [
    { type: _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_3__["MapService"] },
    { type: _services_search_search_service__WEBPACK_IMPORTED_MODULE_7__["SearchService"] },
    { type: _services_fire_service_fire_service__WEBPACK_IMPORTED_MODULE_8__["FireService"] },
    { type: _services_time_time_service__WEBPACK_IMPORTED_MODULE_16__["TimeService"] }
];
HeatmapComponent = HeatmapComponent_1 = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_15__["Component"])({
        selector: 'app-heatmap',
        template: __webpack_require__(/*! raw-loader!./heatmap.component.html */ "./node_modules/raw-loader/index.js!./src/app/map/heatmap/heatmap.component.html"),
        styles: [__webpack_require__(/*! ./heatmap.component.css */ "./src/app/map/heatmap/heatmap.component.css")]
    })
], HeatmapComponent);



/***/ }),

/***/ "./src/app/map/layers/fire.region.layer.ts":
/*!*************************************************!*\
  !*** ./src/app/map/layers/fire.region.layer.ts ***!
  \*************************************************/
/*! exports provided: FireRegionLayer */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FireRegionLayer", function() { return FireRegionLayer; });
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! leaflet/dist/leaflet.css */ "./node_modules/leaflet/dist/leaflet.css");
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../services/map-service/map.service */ "./src/app/services/map-service/map.service.ts");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! leaflet-maskcanvas */ "./node_modules/leaflet-maskcanvas/dist/L.GridLayer.MaskCanvas.js");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! leaflet-velocity-ts */ "./node_modules/leaflet-velocity-ts/dist/leaflet-velocity.js");
/* harmony import */ var leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _services_fire_service_fire_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/fire-service/fire.service */ "./src/app/services/fire-service/fire.service.ts");
/* harmony import */ var _services_time_time_service__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../../services/time/time.service */ "./src/app/services/time/time.service.ts");







class FireRegionLayer {
    constructor(mainControl, mapService, map, fireService, timeService) {
        this.mainControl = mainControl;
        this.mapService = mapService;
        this.map = map;
        this.fireService = fireService;
        this.timeService = timeService;
        this.timeRangeChangeFirePolygonHandler = () => {
            // processes given time data from time-series
            const [dateStartInMs, dateEndInMs] = this.timeService.getRangeDate();
            this.dateStartInISO = new Date(dateStartInMs).toISOString();
            this.dateEndInISO = new Date(dateEndInMs).toISOString();
            this.getFirePolygon(this.dateStartInISO, this.dateEndInISO);
        };
        this.getFirePolygon = (start, end) => {
            // sends request to the map service based on the start/end time and the current screen map boundaries
            const zoom = this.map.getZoom();
            let size;
            if (zoom < 8) {
                size = 4;
            }
            else if (zoom < 9) {
                size = 3;
            }
            else {
                size = 2;
            }
            const bound = this.map.getBounds();
            const boundNE = { lat: bound._northEast.lat, lon: bound._northEast.lng };
            const boundSW = { lat: bound._southWest.lat, lon: bound._southWest.lng };
            this.mapService.getFirePolygonData(boundNE, boundSW, size, start, end).subscribe(this.firePolygonDataHandler);
        };
        this.firePolygonDataHandler = (data) => {
            // adds the fire polygon to the map, the accuracy is based on the zoom level
            if (!this.map.hasLayer(this.firePolygon) && this.firePolygon) {
                return;
            }
            if (this.firePolygon) {
                this.map.removeLayer(this.firePolygon);
                this.mainControl.removeLayer(this.firePolygon);
            }
            if (this.map.getZoom() < 8) {
                const fireLabelList = [];
                for (const fireObject of data.features) {
                    const latlng = [fireObject.geometry.coordinates[1], fireObject.geometry.coordinates[0]];
                    const size = this.map.getZoom() * this.map.getZoom();
                    const fireIcon = L.icon({
                        iconUrl: 'assets/image/pixelfire.gif',
                        iconSize: [size, size],
                    });
                    const marker = L.marker(latlng, { icon: fireIcon }).bindPopup(this.popUpContentZoomIn(fireObject));
                    fireLabelList.push(marker);
                }
                this.firePolygon = L.layerGroup(fireLabelList);
                this.mainControl.addOverlay(this.firePolygon, 'Fire polygon');
                this.map.addLayer(this.firePolygon);
                this.firePolygon.bringToFront();
            }
            else {
                this.firePolygon = L.geoJson(data, {
                    style: this.style,
                    onEachFeature: this.onEachFeature
                });
                this.mainControl.addOverlay(this.firePolygon, 'Fire polygon');
                this.map.addLayer(this.firePolygon);
                this.firePolygon.bringToFront();
            }
        };
        this.popUpContentZoomIn = (fireObject) => {
            // creates css style for the pop up content
            const fireInfoTemplate = jquery__WEBPACK_IMPORTED_MODULE_4__('<div />');
            // tslint:disable-next-line:max-line-length
            fireInfoTemplate.html('<button href="#" class="button-action" ' +
                'style="color: #ff8420; font-family: "Dosis", Arial, Helvetica, sans-serif">Zoom In</button><br>')
                .on('click', '.button-action', () => {
                // when the fire pop up is triggered, go into firePolygonZoomInDataHandler which handels the zoom in
                this.fireObjectInfo = fireObject;
                this.fireService.searchFirePolygon(fireObject.id, 2).subscribe(this.firePolygonZoomInDataHandler);
            });
            const content = FireRegionLayer.formatPopUpContent(fireObject);
            fireInfoTemplate.append(content);
            return fireInfoTemplate[0];
        };
        this.firePolygonZoomInDataHandler = (data) => {
            // zooms in to the fire polygon and adds a pop up
            const bbox = data[0].bbox.coordinates[0];
            const firePolygonLL = [];
            for (const item of bbox) {
                // changes the lat and lng because the geojson format is different to the leaflet latlng format
                firePolygonLL.push([parseFloat(item[1]), parseFloat(item[0])]);
            }
            this.map.fitBounds(firePolygonLL);
            this.fireZoomOutPopup = L.popup({ autoClose: false, closeOnClick: false })
                .setLatLng(this.map.getCenter())
                .setContent(this.popUpContentZoomOut(this.fireObjectInfo))
                .openOn(this.map);
        };
        this.popUpContentZoomOut = (fireObject) => {
            // creates css style for the pop up content
            const fireInfoTemplate = jquery__WEBPACK_IMPORTED_MODULE_4__('<div />');
            const fireReplaceTemplate = jquery__WEBPACK_IMPORTED_MODULE_4__('<div />');
            // tslint:disable-next-line:max-line-length
            fireInfoTemplate.html('<button href="#" class="button-action" style="color: #ff8420; ' +
                'font-family: "Dosis", Arial, Helvetica, sans-serif">Zoom Out</button><br>')
                .on('click', '.button-action', () => {
                this.map.setView([33.64, -117.84], 5);
            });
            // tslint:disable-next-line:max-line-length
            fireReplaceTemplate.html('<button href="#" class="button-replace" style="color: #ff8420; ' +
                'font-family: "Dosis", Arial, Helvetica, sans-serif">Show Fire for Each Day</button><br>')
                .on('click', '.button-replace', () => {
                this.fireService.searchSeparatedFirePolygon(fireObject.id, 2)
                    .subscribe(this.firePolygonDataHandler);
            });
            const content = FireRegionLayer.formatPopUpContent(fireObject);
            fireInfoTemplate.append(fireReplaceTemplate);
            fireInfoTemplate.append(content);
            return fireInfoTemplate[0];
        };
        this.getFirePolygonOnceMoved = () => {
            // calls this every time the map is moved
            if (this.dateStartInISO && this.dateEndInISO) {
                this.getFirePolygon(this.dateStartInISO, this.dateEndInISO);
            }
            // removes the popout sticked to the fire polygon when zoomed out to a certain level
            if (this.fireZoomOutPopup && this.map.getZoom() < 8) {
                this.map.closePopup(this.fireZoomOutPopup);
            }
        };
        this.sendFireToFrontHandler = () => {
            // sends fire to the front layer
            if (this.firePolygon) {
                this.firePolygon.bringToFront();
            }
        };
        this.style = (feature) => {
            // style for the boundary layers
            return {
                fillColor: this.getColor(feature.properties.density),
                weight: 2,
                opacity: 0.8,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.5
            };
        };
        this.getColor = (density) => {
            // color for the fire polygon layers
            // switch (true) {
            //     case (density > 1000):
            //         return '#802403';
            //     case (density > 500):
            //         return '#BD0026';
            //     case (density > 200):
            //         return '#E31A1C';
            //     case (density > 100):
            //         return '#FC4E2A';
            //     case (density > 50):
            //         return '#FD8D3C';
            //     case (density > 20):
            //         return '#FEB24C';
            //     case (density > 10):
            //         return '#FED976';
            //     default:
            //         return '#FFEDA0';
            // }
            return '#fff10d';
        };
        this.onEachFeature = (feature, layer) => {
            // controls the interaction between the mouse and the map
            layer.on({
                mouseover: this.highlightFeature,
                mouseout: this.resetHighlight,
                click: this.zoomToFeature
            });
        };
        this.highlightFeature = (event) => {
            // highlights the region when the mouse moves over the region
            const layer = event.target;
            layer.setStyle({
                weight: 5,
                color: '#e37927',
                dashArray: '',
                fillOpacity: 0.7
            });
        };
        this.resetHighlight = (event) => {
            // gets rid of the highlight when the mouse moves out of the region
            this.firePolygon.resetStyle(event.target);
        };
        this.zoomToFeature = (event) => {
            // zooms to a region when the region is clicked
            this.map.fitBounds(event.target.getBounds());
        };
        this.mapService.sendFireToFront.subscribe(this.sendFireToFrontHandler);
        this.map.on('zoomend, moveend', this.getFirePolygonOnceMoved);
        this.timeRangeChangeFirePolygonHandler();
    }
    static formatPopUpContent(fireObject) {
        return '\n <div class="fire">\n '
            + '      <span class="name" style=\'color: #ff8420;\'> '
            + 'Fire Name: ' + fireObject.properties.name
            + '      </span><br> '
            + '      <span class="fire-starttime" style=\'color: #ff8420;\'>'
            + 'Fire Start Time: ' + fireObject.properties.starttime
            + '      </span><br>\n	 '
            + '      <span class="fire-endtime" style=\'color: #ff8420;\'>'
            + 'Fire End Time: ' + fireObject.properties.endtime
            + '      </span><br>\n	 '
            + '      <span class="fire-area" style=\'color: #ff8420;\'>'
            + 'Fire Area: ' + fireObject.properties.area + ' acres'
            + '      </span><br>\n	 '
            + '<span class="fire-agency" style=\'color: #ff8420;\'>'
            + 'Fire Agency: ' + fireObject.properties.agency
            + '      </span><br>\n	 '
            + '</div>\n';
    }
}
FireRegionLayer.ctorParameters = () => [
    null,
    { type: _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_1__["MapService"] },
    null,
    { type: _services_fire_service_fire_service__WEBPACK_IMPORTED_MODULE_5__["FireService"] },
    { type: _services_time_time_service__WEBPACK_IMPORTED_MODULE_6__["TimeService"] }
];


/***/ }),

/***/ "./src/app/map/layers/fire.tweet.layer.ts":
/*!************************************************!*\
  !*** ./src/app/map/layers/fire.tweet.layer.ts ***!
  \************************************************/
/*! exports provided: FireTweetLayer */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FireTweetLayer", function() { return FireTweetLayer; });
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! leaflet/dist/leaflet.css */ "./node_modules/leaflet/dist/leaflet.css");
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../services/map-service/map.service */ "./src/app/services/map-service/map.service.ts");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! leaflet-maskcanvas */ "./node_modules/leaflet-maskcanvas/dist/L.GridLayer.MaskCanvas.js");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! leaflet-velocity-ts */ "./node_modules/leaflet-velocity-ts/dist/leaflet-velocity.js");
/* harmony import */ var leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var rxjs__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! rxjs */ "./node_modules/rxjs/_esm2015/index.js");
/* harmony import */ var _services_time_time_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/time/time.service */ "./src/app/services/time/time.service.ts");
/**
 * @author: Yuan Fu <yuanf9@uci.edu>
 * @author: (Hugo) Qiaonan Huang <qiaonanh@uci.edu>
 */






class FireTweetLayer {
    constructor(mainControl, mapService, map, timeService) {
        this.mainControl = mainControl;
        this.mapService = mapService;
        this.map = map;
        this.timeService = timeService;
        this.tweetData = [];
        this.currentBounds = null;
        this.currentMarker = null;
        this.scaleX = 0;
        this.scaleY = 0;
        this.mouseOverPointI = 0;
        this.tempDataWithID = [];
        this.timer = null;
        this.tweetDataHandler = (tweets) => {
            /**
             *  Display current tweet data as red dots on canvas
             *
             *  Just used geolocation property of the objects given to display
             *
             *  @param {Object} list of tweet object with geolocation, time of tweet, id of tweet
             */
            this.tweetData = tweets;
            this.tweetLayer = L.TileLayer.maskCanvas({
                radius: 10,
                useAbsoluteRadius: true,
                color: '#000',
                opacity: 1,
                noMask: true,
                lineColor: '#e25822'
            });
            const tempData = [];
            this.tweetData.forEach(tweet => {
                tempData.push([tweet.lat, tweet.long]);
            });
            this.tweetLayer.setData(tempData);
            this.mainControl.addOverlay(this.tweetLayer, 'Fire tweet');
            this.timeRangeChangeHandler();
        };
        this.timeRangeChangeHandler = () => {
            /**
             *  Set tweetLayer data satisfy the time range
             *
             *  Filter out tweets which not satisfy the time range selection;
             *  store qualified tweets with their id in list 'tempDataWithID' for later content display usage
             */
            const tempData = [];
            this.tempDataWithID = [];
            const [startDateInMs, endDateInMs] = this.timeService.getRangeDate();
            this.tweetData.forEach(tweet => {
                const time = new Date(tweet.create_at).getTime();
                if (time > startDateInMs && time < endDateInMs) {
                    tempData.push([tweet.lat, tweet.long]);
                    this.tempDataWithID.push([tweet.lat, tweet.long, tweet.id]);
                }
            });
            this.tweetLayer.setData(tempData);
        };
        // This is the overlay controller defined in constructor
        this.mapService.getFireTweetData().subscribe(this.tweetDataHandler);
        this.map.on('overlayadd', (event) => {
            if (event.name === 'Fire tweet') {
                this.map.on('mousemove', e => this.onMapMouseMove(e));
            }
        });
        this.map.on('overlayremove', (event) => {
            if (event.name === 'Fire tweet') {
                this.map.removeLayer(this.currentMarker);
                this.currentMarker = undefined;
            }
        });
    }
    // TODO: REWRITE IT!!!!!!
    static translateTweetDataToShow(tweetJSON) {
        /**
         *  Static format for each tweet's popup
         *
         *  First try to read info and catch if not exist;
         *  then presents all the content of a tweet with format
         *
         *  @param {Object} one single tweet object with id, user, user profile, text, time,and image
         *
         *  @return a html string which give format and customized look of the popup
         */
        // read info and catch err
        let tweetid = '';
        try {
            tweetid = tweetJSON.id;
        }
        catch (e) {
            // tweet id missing in this Tweet.
        }
        let userName = '';
        try {
            userName = tweetJSON.user;
        }
        catch (e) {
            // userName missing in this Tweet.
        }
        let userPhotoUrl = '';
        try {
            // 'http://p1.qhimg.com/t015b79f2dd6a285745.jpg'
            userPhotoUrl = tweetJSON.profilePic;
        }
        catch (e) {
            // user.profile_image_url missing in this Tweet.
        }
        let tweetText = '';
        try {
            tweetText = tweetJSON.text;
        }
        catch (e) {
            // Text missing in this Tweet.
        }
        let tweetTime = '';
        try {
            const createdAt = new Date(tweetJSON.create_at);
            tweetTime = createdAt.toISOString();
        }
        catch (e) {
            // Time missing in this Tweet.
        }
        let tweetLink = '';
        try {
            tweetLink = 'https://twitter.com/' + userName + '/status/' + tweetid;
        }
        catch (e) {
            // tweetLink missing in this Tweet.
        }
        let imageUrl = '';
        try {
            imageUrl = tweetJSON.image; // 'https://pbs.twimg.com/media/DE6orpqVYAAeCYz.jpg'
        }
        catch (e) {
            // imageLink missing in this Tweet.
        }
        let tweetTemplate;
        // handles exceptions:
        if (tweetText === '' || null || undefined) {
            tweetTemplate = '\n'
                + '<div>'
                + 'Fail to get Tweets data.'
                + '</div>\n';
        }
        else {
            // presents all the content of a tweet with format
            tweetTemplate = '\n'
                + '<div class="tweet">\n '
                + '  <div class="tweet-body">'
                + '    <div class="user-info"> '
                + '      <img src="'
                + userPhotoUrl
                + '" onerror=" this.src=\'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRJIsOFUYD9y2r12OzjDoEe5I1uhhF-gfVj5WGIqg8MzNBVzSogRw\'" style="width: 32px; display: inline; ">\n'
                + '      <span class="name" style=\'color: #0e90d2; font-weight: bold\'> '
                + userName
                + '      </span> '
                + '    </div>\n	'
                + '    <span class="tweet-time" style=\'color: darkgray\'>'
                + tweetTime
                + '    <br></span>\n	 '
                + '    <span class="tweet-text" style=\'color: #0f0f0f\'>'
                + tweetText
                + '    </span><br>\n	 '
                + '\n <a href="'
                + tweetLink
                + '"> '
                + tweetLink
                + '</a>'
                + '  </div>\n	'
                + '      <img src="'
                + imageUrl
                + '" onerror=" this.src=\'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT1oYihdIC_G2vCN1dr3B6t5Y1EVKRLmD5qCrrtV_1eE3aJXpYv\'" style="height: 100px; ">\n'
                + '</div>\n';
        }
        return tweetTemplate;
    }
    idOverPoint(x, y) {
        /**
         *  Determine if the mouse on a tweet, if so, return id
         *
         *  Store qualified tweets with their id in list 'tempDataWithID' for later content display usage;
         *  scan the list 'tempDataWithID' to check which dot is the mouse on;
         *  identify is the mouse almost over a tweet dot;
         *  rescale the distance between mouse and the dot, since no user can mouse on exactly the pixel of the dot
         *
         *  @param {type} lat,long of current mouse location
         *
         *  @return [int,id] a list gives a index of this tweet and the id of this tweet, if mouse not over the tweet, return [-1, null]
         */
        for (let i = 0; i < this.tempDataWithID.length; i += 1) {
            const distX = Math.abs((this.tempDataWithID[i][0] - x) / this.scaleX);
            const distY = Math.abs((this.tempDataWithID[i][1] - y) / this.scaleY);
            // if the mouse almost over a tweet dot, use this to rescale the distance
            if (distX <= 0.001 && distY <= 0.001) {
                return [i, this.tempDataWithID[i][2]];
            }
        }
        return [-1, null];
    }
    onMapMouseMove(event) {
        /**
         *  Timer to determine mouseon time
         *
         *  If mouse hang over a dot for over 250ms, fire 'onMapMouseIntent' function
         *
         *  @param {object} lat,long of current mouse location
         */
        if (this.map.hasLayer(this.tweetLayer)) {
            const duration = 250;
            if (this.timer !== null) {
                clearTimeout(this.timer);
                this.timer = null;
            }
            this.timer = setTimeout(L.Util.bind(() => {
                Object(rxjs__WEBPACK_IMPORTED_MODULE_4__["of"])(event).subscribe((ev) => this.onMapMouseIntent(ev));
                this.timer = null;
            }, this), duration);
        }
    }
    onMapMouseIntent(e) {
        /**
         *  Generate a red circle marker on the selected tweet dot
         *
         *  First make sure the scale metrics are updated;
         *  if mouse over a new point, show the Popup Tweet, if previous Marker is not null, destroy;
         *
         *  @param {object} lat,long of current mouse location
         */
        // make sure the scale metrics are updated
        if (this.currentBounds === null || this.scaleX === 0 || this.scaleY === 0) {
            this.currentBounds = this.map.getBounds();
            this.scaleX = Math.abs(this.currentBounds.getEast()
                - this.currentBounds.getWest());
            this.scaleY = Math.abs(this.currentBounds.getNorth()
                - this.currentBounds.getSouth());
        }
        const iandID = this.idOverPoint(e.latlng.lat, e.latlng.lng);
        const i = iandID[0];
        // if mouse over a new point, show the Popup Tweet!
        if (i >= 0 && this.mouseOverPointI !== i) {
            this.mouseOverPointI = i;
            // (1) If previous Marker is not null, destroy it.
            if (this.currentMarker != null) {
                this.map.removeLayer(this.currentMarker);
            }
            // (2) Create a new Marker to highlight the point.
            this.currentMarker = L.circleMarker(e.latlng, {
                radius: 7,
                color: '#fa4c3c',
                weight: 3,
                fillColor: '#f7ada6',
                fillOpacity: 1.0
            }).addTo(this.map);
            this.mapService.getIntentTweetData(iandID[1]).subscribe(data => this.IntentTweetPopup(data));
        }
    }
    IntentTweetPopup(data) {
        /**
         *  Make current red circle marker clickable to show a popup tweet content
         *
         *  @param {object} one tweet object with id, user, user profile, text, time,and image
         */
        this.currentMarker.bindPopup(FireTweetLayer.translateTweetDataToShow(data));
    }
    recentTweetLoadHandler(data) {
        /**
         *  Shows recent tweet within several days as an animated bird marker
         *
         *  @param {list} a list of tweet object with id, user, user profile, text, time,and image
         */
        const fireEventList = [];
        for (const ev of data.slice(0, 150)) {
            const point = [ev.lat, ev.long];
            const size = 12.5;
            const fireIcon = L.icon({
                iconUrl: 'assets/image/perfectBird.gif',
                iconSize: [size, size],
            });
            const tweetContent = FireTweetLayer.translateTweetDataToShow(ev);
            // const tweetContent = 'CONTENT: ' + ev[4] + '<br/>TIME: ' + ev[2] + '<br/>TWEETID#: ' + ev[3];
            const marker = L.marker(point, { icon: fireIcon }).bindPopup(tweetContent);
            fireEventList.push(marker);
        }
        const fireEvents = L.layerGroup(fireEventList);
        this.mainControl.addOverlay(fireEvents, 'Recent tweet (within 2 days)');
    }
}
FireTweetLayer.ctorParameters = () => [
    null,
    { type: _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_1__["MapService"] },
    null,
    { type: _services_time_time_service__WEBPACK_IMPORTED_MODULE_5__["TimeService"] }
];


/***/ }),

/***/ "./src/app/map/layers/location.boundary.layer.ts":
/*!*******************************************************!*\
  !*** ./src/app/map/layers/location.boundary.layer.ts ***!
  \*******************************************************/
/*! exports provided: LocationBoundaryLayer */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LocationBoundaryLayer", function() { return LocationBoundaryLayer; });
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! leaflet/dist/leaflet.css */ "./node_modules/leaflet/dist/leaflet.css");
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../services/map-service/map.service */ "./src/app/services/map-service/map.service.ts");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! leaflet-maskcanvas */ "./node_modules/leaflet-maskcanvas/dist/L.GridLayer.MaskCanvas.js");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! leaflet-velocity-ts */ "./node_modules/leaflet-velocity-ts/dist/leaflet-velocity.js");
/* harmony import */ var leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3__);




class LocationBoundaryLayer {
    constructor(mainControl, mapService, map) {
        this.mainControl = mainControl;
        this.mapService = mapService;
        this.map = map;
        this.getBoundary = () => {
            // gets the screen bounds and zoom level to get the corresponding geo boundaries from database
            const zoom = this.map.getZoom();
            const bound = this.map.getBounds();
            const boundNE = { lat: bound._northEast.lat, lon: bound._northEast.lng };
            const boundSW = { lat: bound._southWest.lat, lon: bound._southWest.lng };
            // tslint:disable-next-line:one-variable-per-declaration
            let showCityLevel, showStateLevel, showCountyLevel;
            // the boundary display with zoom levels is defined arbitrarily
            if (zoom < 9) {
                showCityLevel = false;
                showCountyLevel = false;
                showStateLevel = true;
            }
            else if (zoom < 8) {
                showCityLevel = false;
                showCountyLevel = true;
                showStateLevel = true;
            }
            else {
                showCityLevel = true;
                showCountyLevel = true;
                showStateLevel = true;
            }
            this.mapService.getBoundaryData(showStateLevel, showCountyLevel, showCityLevel, boundNE, boundSW)
                .subscribe(this.getBoundaryScreenDataHandler);
        };
        this.getBoundaryScreenDataHandler = (data) => {
            // adds boundary layer onto the map
            if (!this.map.hasLayer(this.boundaryLayer) && this.boundaryLayer) {
                return;
            }
            // remove previous overlay
            if (this.boundaryLayer) {
                this.map.removeLayer(this.boundaryLayer);
                this.mainControl.removeLayer(this.boundaryLayer);
            }
            this.boundaryLayer = L.geoJson(data, {
                style: this.style,
                onEachFeature: this.onEachFeature,
            });
            this.mainControl.addOverlay(this.boundaryLayer, 'Boundary');
            this.map.addLayer(this.boundaryLayer);
            this.mapService.sendFireToFront.emit();
        };
        this.style = (feature) => {
            // style for the boundary layers
            return {
                fillColor: this.getColor(feature.properties.density),
                weight: 2,
                opacity: 0.8,
                color: 'white',
                dashArray: '3',
                fillOpacity: 0.5
            };
        };
        this.getColor = (density) => {
            // color for the boundary layers
            // TODO: remove this func
            switch (true) {
                case (density > 1000):
                    return '#fd3208';
                case (density > 500):
                    return '#f40031';
                case (density > 200):
                    return '#f74d1a';
                case (density > 100):
                    return '#fc5a0a';
                case (density > 50):
                    return '#fd810b';
                case (density > 20):
                    return '#fe046a';
                default:
                    return '#fe0b2e';
            }
        };
        this.onEachFeature = (feature, layer) => {
            // controls the interaction between the mouse and the map
            layer.on({
                mouseover: this.highlightFeature,
                mouseout: this.resetHighlight,
                click: this.zoomToFeature
            });
        };
        this.highlightFeature = (event) => {
            // highlights the region when the mouse moves over the region
            const layer = event.target;
            layer.setStyle({
                weight: 5,
                color: '#e37927',
                dashArray: '',
                fillOpacity: 0.7
            });
            this.mapService.searchNameLoaded.emit(event.target.feature.properties.name);
            this.mapService.hoverMarkerLoaded.emit(event);
        };
        this.resetHighlight = (event) => {
            // gets rid of the highlight when the mouse moves out of the region
            this.boundaryLayer.resetStyle(event.target);
            this.mapService.searchNameLoaded.emit('');
            this.mapService.markerRemove.emit();
        };
        this.zoomToFeature = (event) => {
            // zooms to a region when the region is clicked
            this.map.fitBounds(event.target.getBounds());
        };
        this.getBoundary();
        this.map.on('zoomend, moveend', this.getBoundary);
    }
}
LocationBoundaryLayer.ctorParameters = () => [
    null,
    { type: _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_1__["MapService"] },
    null
];


/***/ }),

/***/ "./src/app/map/layers/location.marker.ts":
/*!***********************************************!*\
  !*** ./src/app/map/layers/location.marker.ts ***!
  \***********************************************/
/*! exports provided: LocationMarkerLayer */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LocationMarkerLayer", function() { return LocationMarkerLayer; });
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! leaflet/dist/leaflet.css */ "./node_modules/leaflet/dist/leaflet.css");
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../services/map-service/map.service */ "./src/app/services/map-service/map.service.ts");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! leaflet-maskcanvas */ "./node_modules/leaflet-maskcanvas/dist/L.GridLayer.MaskCanvas.js");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! leaflet-velocity-ts */ "./node_modules/leaflet-velocity-ts/dist/leaflet-velocity.js");
/* harmony import */ var leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3__);




class LocationMarkerLayer {
    constructor(mainControl, mapService, map) {
        this.mainControl = mainControl;
        this.mapService = mapService;
        this.map = map;
        this.markerInputEventHandler = (value) => {
            // creates the marker on the location being searched after zoomed in
            const centerLatlng = value[0];
            const userInput = value[1];
            const zoom = this.map.getZoom();
            if (this.theSearchMarker) {
                // removes previous marker
                this.map.removeControl(this.theSearchMarker);
            }
            // creates the name label
            const divIcon = L.divIcon({
                html: '<span style=\'color:#ffffff;font-size:18px;\' id=\'userInput\'>' + userInput + '</span>',
                iconSize: [this.map.getZoom(), this.map.getZoom()],
            });
            this.theSearchMarker = L.marker(new L.LatLng(centerLatlng[0], centerLatlng[1]), { icon: divIcon }).addTo(this.map);
            this.setLabelStyle(this.theSearchMarker); // sets the label style
        };
        this.markerMouseHoverEventHandler = (event) => {
            // shows the name label when the area is highlighted
            const layer = event.target;
            const divIcon = L.divIcon({
                html: '<span style=\'color:#ffffff;font-size: 18px;\'>' + layer.feature.properties.name + '</span>',
                iconSize: [this.map.getZoom(), this.map.getZoom()],
            });
            const centerLatLng = layer.getCenter();
            if (this.theSearchMarker) {
                this.map.removeControl(this.theSearchMarker);
            }
            if (this.theHighlightMarker) {
                this.map.removeControl(this.theHighlightMarker);
            }
            this.theHighlightMarker = L.marker(new L.LatLng(centerLatLng.lat, centerLatLng.lng), { icon: divIcon }).addTo(this.map);
            this.setLabelStyle(this.theHighlightMarker);
        };
        this.markerMouseHoverRemoveHandler = () => {
            if (this.theHighlightMarker) {
                this.map.removeControl(this.theHighlightMarker);
            }
        };
        this.setLabelStyle = (marker) => {
            // sets the name label style
            marker.getElement().style.backgroundColor = 'transparent';
            marker.getElement().style.border = 'transparent';
            marker.getElement().style.fontFamily = 'arial';
            marker.getElement().style.webkitTextStroke = '#ff8420';
            marker.getElement().style.webkitTextStrokeWidth = '0.5px';
        };
        this.mapService.searchMarkerLoaded.subscribe(this.markerInputEventHandler);
        this.mapService.hoverMarkerLoaded.subscribe(this.markerMouseHoverEventHandler);
        this.mapService.markerRemove.subscribe(this.markerMouseHoverRemoveHandler);
    }
}
LocationMarkerLayer.ctorParameters = () => [
    null,
    { type: _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_1__["MapService"] },
    null
];


/***/ }),

/***/ "./src/app/map/layers/wind.layer.ts":
/*!******************************************!*\
  !*** ./src/app/map/layers/wind.layer.ts ***!
  \******************************************/
/*! exports provided: WindLayer */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "WindLayer", function() { return WindLayer; });
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! leaflet/dist/leaflet.css */ "./node_modules/leaflet/dist/leaflet.css");
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ../../services/map-service/map.service */ "./src/app/services/map-service/map.service.ts");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! leaflet-maskcanvas */ "./node_modules/leaflet-maskcanvas/dist/L.GridLayer.MaskCanvas.js");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! leaflet-velocity-ts */ "./node_modules/leaflet-velocity-ts/dist/leaflet-velocity.js");
/* harmony import */ var leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(leaflet_velocity_ts__WEBPACK_IMPORTED_MODULE_3__);




class WindLayer {
    constructor(mainControl, mapService) {
        this.mainControl = mainControl;
        this.mapService = mapService;
        this.windDataHandler = (wind) => {
            // there's not much document about leaflet-velocity.
            // all we got is an example usage from
            // github.com/0nza1101/leaflet-velocity-ts
            const velocityLayer = L.velocityLayer({
                displayValues: true,
                displayOptions: {
                    position: 'bottomleft',
                    emptyString: 'No velocity data',
                    angleConvention: 'bearingCW',
                    velocityType: 'Global Wind',
                    displayPosition: 'bottomleft',
                    displayEmptyString: 'No wind data',
                    speedUnit: 'm/s'
                },
                data: wind,
                maxVelocity: 12 // affect color and animation speed of wind
            });
            this.mainControl.addOverlay(velocityLayer, 'Global wind');
        };
        this.mapService.getWindData().subscribe(this.windDataHandler);
    }
}
WindLayer.ctorParameters = () => [
    null,
    { type: _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_1__["MapService"] }
];


/***/ }),

/***/ "./src/app/map/location-name-display/location-name-display.component.css":
/*!*******************************************************************************!*\
  !*** ./src/app/map/location-name-display/location-name-display.component.css ***!
  \*******************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "#info {\n    padding: 6px 8px;\n    font: 14px/16px Arial, Helvetica, sans-serif;\n    color: #ff8420;\n    background: white;\n    background: rgba(255, 255, 255, 0.8);\n    box-shadow: 0 0 15px rgba(251, 227, 0, 0.2);\n    border-radius: 5px;\n    position: absolute;\n    top: 1%;\n    left: 10%;\n    z-index: 1000000;\n}\n\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvbWFwL2xvY2F0aW9uLW5hbWUtZGlzcGxheS9sb2NhdGlvbi1uYW1lLWRpc3BsYXkuY29tcG9uZW50LmNzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtJQUNJLGdCQUFnQjtJQUNoQiw0Q0FBNEM7SUFDNUMsY0FBYztJQUNkLGlCQUFpQjtJQUNqQixvQ0FBb0M7SUFDcEMsMkNBQTJDO0lBQzNDLGtCQUFrQjtJQUNsQixrQkFBa0I7SUFDbEIsT0FBTztJQUNQLFNBQVM7SUFDVCxnQkFBZ0I7QUFDcEIiLCJmaWxlIjoic3JjL2FwcC9tYXAvbG9jYXRpb24tbmFtZS1kaXNwbGF5L2xvY2F0aW9uLW5hbWUtZGlzcGxheS5jb21wb25lbnQuY3NzIiwic291cmNlc0NvbnRlbnQiOlsiI2luZm8ge1xuICAgIHBhZGRpbmc6IDZweCA4cHg7XG4gICAgZm9udDogMTRweC8xNnB4IEFyaWFsLCBIZWx2ZXRpY2EsIHNhbnMtc2VyaWY7XG4gICAgY29sb3I6ICNmZjg0MjA7XG4gICAgYmFja2dyb3VuZDogd2hpdGU7XG4gICAgYmFja2dyb3VuZDogcmdiYSgyNTUsIDI1NSwgMjU1LCAwLjgpO1xuICAgIGJveC1zaGFkb3c6IDAgMCAxNXB4IHJnYmEoMjUxLCAyMjcsIDAsIDAuMik7XG4gICAgYm9yZGVyLXJhZGl1czogNXB4O1xuICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgICB0b3A6IDElO1xuICAgIGxlZnQ6IDEwJTtcbiAgICB6LWluZGV4OiAxMDAwMDAwO1xufVxuIl19 */"

/***/ }),

/***/ "./src/app/map/location-name-display/location-name-display.component.ts":
/*!******************************************************************************!*\
  !*** ./src/app/map/location-name-display/location-name-display.component.ts ***!
  \******************************************************************************/
/*! exports provided: LocationNameDisplayComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "LocationNameDisplayComponent", function() { return LocationNameDisplayComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! leaflet/dist/leaflet.css */ "./node_modules/leaflet/dist/leaflet.css");
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! leaflet-maskcanvas */ "./node_modules/leaflet-maskcanvas/dist/L.GridLayer.MaskCanvas.js");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/map-service/map.service */ "./src/app/services/map-service/map.service.ts");
/* harmony import */ var _services_search_search_service__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ../../services/search/search.service */ "./src/app/services/search/search.service.ts");






let LocationNameDisplayComponent = class LocationNameDisplayComponent {
    constructor(mapService, searchService) {
        this.mapService = mapService;
        this.searchService = searchService;
        // OPTIMIZE: combine these two handlers
        this.locationInputEventHandler = ([[data], value]) => {
            document.getElementById('info').innerHTML = 'location name: ' + value;
        };
        this.locationMouseHoverEventHandler = (value) => {
            document.getElementById('info').innerHTML = 'location name: ' + value;
        };
    }
    ngOnInit() {
        this.searchService.searchDataLoaded.subscribe(this.locationInputEventHandler);
        this.mapService.searchNameLoaded.subscribe(this.locationMouseHoverEventHandler);
    }
};
LocationNameDisplayComponent.ctorParameters = () => [
    { type: _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_4__["MapService"] },
    { type: _services_search_search_service__WEBPACK_IMPORTED_MODULE_5__["SearchService"] }
];
LocationNameDisplayComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-location-name-display',
        template: __webpack_require__(/*! raw-loader!./location-name-display.component.html */ "./node_modules/raw-loader/index.js!./src/app/map/location-name-display/location-name-display.component.html"),
        styles: [__webpack_require__(/*! ./location-name-display.component.css */ "./src/app/map/location-name-display/location-name-display.component.css")]
    })
], LocationNameDisplayComponent);



/***/ }),

/***/ "./src/app/map/map.module.ts":
/*!***********************************!*\
  !*** ./src/app/map/map.module.ts ***!
  \***********************************/
/*! exports provided: MapModule */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MapModule", function() { return MapModule; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common */ "./node_modules/@angular/common/fesm2015/common.js");
/* harmony import */ var _asymmetrik_ngx_leaflet__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @asymmetrik/ngx-leaflet */ "./node_modules/@asymmetrik/ngx-leaflet/dist/index.js");
/* harmony import */ var _heatmap_heatmap_component__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./heatmap/heatmap.component */ "./src/app/map/heatmap/heatmap.component.ts");
/* harmony import */ var _sidebar_sidebar_component__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./sidebar/sidebar.component */ "./src/app/map/sidebar/sidebar.component.ts");
/* harmony import */ var _time_series_time_series_component__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ./time-series/time-series.component */ "./src/app/map/time-series/time-series.component.ts");
/* harmony import */ var _tab_tab_component__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./tab/tab.component */ "./src/app/map/tab/tab.component.ts");
/* harmony import */ var _sidebar_temperature_range_slider_temperature_range_slider_component__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./sidebar/temperature-range-slider/temperature-range-slider.component */ "./src/app/map/sidebar/temperature-range-slider/temperature-range-slider.component.ts");
/* harmony import */ var _search_bar_search_component__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./search-bar/search.component */ "./src/app/map/search-bar/search.component.ts");
/* harmony import */ var _angular_material__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @angular/material */ "./node_modules/@angular/material/esm2015/material.js");
/* harmony import */ var _angular_material_select__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @angular/material/select */ "./node_modules/@angular/material/esm2015/select.js");
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _location_name_display_location_name_display_component__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! ./location-name-display/location-name-display.component */ "./src/app/map/location-name-display/location-name-display.component.ts");














let MapModule = class MapModule {
    constructor() {
    }
};
MapModule = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["NgModule"])({
        declarations: [_heatmap_heatmap_component__WEBPACK_IMPORTED_MODULE_4__["HeatmapComponent"], _sidebar_sidebar_component__WEBPACK_IMPORTED_MODULE_5__["SidebarComponent"], _time_series_time_series_component__WEBPACK_IMPORTED_MODULE_6__["TimeSeriesComponent"],
            _sidebar_temperature_range_slider_temperature_range_slider_component__WEBPACK_IMPORTED_MODULE_8__["TemperatureRangeSliderComponent"], _search_bar_search_component__WEBPACK_IMPORTED_MODULE_9__["SearchComponent"], _search_bar_search_component__WEBPACK_IMPORTED_MODULE_9__["SearchComponent"],
            _location_name_display_location_name_display_component__WEBPACK_IMPORTED_MODULE_13__["LocationNameDisplayComponent"], _tab_tab_component__WEBPACK_IMPORTED_MODULE_7__["TabGroupComponent"]],
        exports: [
            _heatmap_heatmap_component__WEBPACK_IMPORTED_MODULE_4__["HeatmapComponent"],
            _sidebar_sidebar_component__WEBPACK_IMPORTED_MODULE_5__["SidebarComponent"],
            _time_series_time_series_component__WEBPACK_IMPORTED_MODULE_6__["TimeSeriesComponent"],
            _sidebar_temperature_range_slider_temperature_range_slider_component__WEBPACK_IMPORTED_MODULE_8__["TemperatureRangeSliderComponent"],
            _search_bar_search_component__WEBPACK_IMPORTED_MODULE_9__["SearchComponent"],
            _tab_tab_component__WEBPACK_IMPORTED_MODULE_7__["TabGroupComponent"],
            _location_name_display_location_name_display_component__WEBPACK_IMPORTED_MODULE_13__["LocationNameDisplayComponent"]
        ],
        imports: [
            _angular_common__WEBPACK_IMPORTED_MODULE_2__["CommonModule"],
            _asymmetrik_ngx_leaflet__WEBPACK_IMPORTED_MODULE_3__["LeafletModule"],
            _angular_material__WEBPACK_IMPORTED_MODULE_10__["MatFormFieldModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_12__["ReactiveFormsModule"],
            _angular_material__WEBPACK_IMPORTED_MODULE_10__["MatAutocompleteModule"],
            _angular_material__WEBPACK_IMPORTED_MODULE_10__["MatInputModule"],
            _angular_forms__WEBPACK_IMPORTED_MODULE_12__["FormsModule"],
            _angular_material_select__WEBPACK_IMPORTED_MODULE_11__["MatSelectModule"],
            _angular_material__WEBPACK_IMPORTED_MODULE_10__["MatTabsModule"],
        ],
    })
], MapModule);



/***/ }),

/***/ "./src/app/map/search-bar/search.component.css":
/*!*****************************************************!*\
  !*** ./src/app/map/search-bar/search.component.css ***!
  \*****************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".example-form {\n    min-width: 100px;\n    max-width: 450px;\n    width: 100%;\n    z-index: 1000000;\n    position: absolute;\n    background-color: white;\n    border: none;\n    color: #ff8420;\n    opacity: 0.9;\n    left: 40%;\n    border-radius: 5px;\n\n}\n\n.example-full-width {\n    width: 100%;\n}\n\n::ng-deep .cdk-overlay-container .cdk-overlay-connected-position-bounding-box .cdk-overlay-pane .mat-autocomplete-panel {\n    /*drop down panel color*/\n    background-color: rgb(255, 255, 255) !important;\n    opacity: 0.9 !important;\n}\n\n::ng-deep .cdk-overlay-container .cdk-overlay-connected-position-bounding-box .cdk-overlay-pane .mat-option {\n    /*drop down options color*/\n    color: #ff8420 !important;\n    font-size: 15px !important;\n\n}\n\n::ng-deep .example-form.ng-untouched.ng-pristine.ng-valid {\n    /*background of the input box*/\n    height: 48px;\n    top: 5%;\n    position: absolute;\n}\n\n::ng-deep .ng-star-inserted {\n    color: #ff8420 !important;\n}\n\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvbWFwL3NlYXJjaC1iYXIvc2VhcmNoLmNvbXBvbmVudC5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7SUFDSSxnQkFBZ0I7SUFDaEIsZ0JBQWdCO0lBQ2hCLFdBQVc7SUFDWCxnQkFBZ0I7SUFDaEIsa0JBQWtCO0lBQ2xCLHVCQUF1QjtJQUN2QixZQUFZO0lBQ1osY0FBYztJQUNkLFlBQVk7SUFDWixTQUFTO0lBQ1Qsa0JBQWtCOztBQUV0Qjs7QUFFQTtJQUNJLFdBQVc7QUFDZjs7QUFFQTtJQUNJLHdCQUF3QjtJQUN4QiwrQ0FBK0M7SUFDL0MsdUJBQXVCO0FBQzNCOztBQUVBO0lBQ0ksMEJBQTBCO0lBQzFCLHlCQUF5QjtJQUN6QiwwQkFBMEI7O0FBRTlCOztBQUVBO0lBQ0ksOEJBQThCO0lBQzlCLFlBQVk7SUFDWixPQUFPO0lBQ1Asa0JBQWtCO0FBQ3RCOztBQUdBO0lBQ0kseUJBQXlCO0FBQzdCIiwiZmlsZSI6InNyYy9hcHAvbWFwL3NlYXJjaC1iYXIvc2VhcmNoLmNvbXBvbmVudC5jc3MiLCJzb3VyY2VzQ29udGVudCI6WyIuZXhhbXBsZS1mb3JtIHtcbiAgICBtaW4td2lkdGg6IDEwMHB4O1xuICAgIG1heC13aWR0aDogNDUwcHg7XG4gICAgd2lkdGg6IDEwMCU7XG4gICAgei1pbmRleDogMTAwMDAwMDtcbiAgICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gICAgYmFja2dyb3VuZC1jb2xvcjogd2hpdGU7XG4gICAgYm9yZGVyOiBub25lO1xuICAgIGNvbG9yOiAjZmY4NDIwO1xuICAgIG9wYWNpdHk6IDAuOTtcbiAgICBsZWZ0OiA0MCU7XG4gICAgYm9yZGVyLXJhZGl1czogNXB4O1xuXG59XG5cbi5leGFtcGxlLWZ1bGwtd2lkdGgge1xuICAgIHdpZHRoOiAxMDAlO1xufVxuXG46Om5nLWRlZXAgLmNkay1vdmVybGF5LWNvbnRhaW5lciAuY2RrLW92ZXJsYXktY29ubmVjdGVkLXBvc2l0aW9uLWJvdW5kaW5nLWJveCAuY2RrLW92ZXJsYXktcGFuZSAubWF0LWF1dG9jb21wbGV0ZS1wYW5lbCB7XG4gICAgLypkcm9wIGRvd24gcGFuZWwgY29sb3IqL1xuICAgIGJhY2tncm91bmQtY29sb3I6IHJnYigyNTUsIDI1NSwgMjU1KSAhaW1wb3J0YW50O1xuICAgIG9wYWNpdHk6IDAuOSAhaW1wb3J0YW50O1xufVxuXG46Om5nLWRlZXAgLmNkay1vdmVybGF5LWNvbnRhaW5lciAuY2RrLW92ZXJsYXktY29ubmVjdGVkLXBvc2l0aW9uLWJvdW5kaW5nLWJveCAuY2RrLW92ZXJsYXktcGFuZSAubWF0LW9wdGlvbiB7XG4gICAgLypkcm9wIGRvd24gb3B0aW9ucyBjb2xvciovXG4gICAgY29sb3I6ICNmZjg0MjAgIWltcG9ydGFudDtcbiAgICBmb250LXNpemU6IDE1cHggIWltcG9ydGFudDtcblxufVxuXG46Om5nLWRlZXAgLmV4YW1wbGUtZm9ybS5uZy11bnRvdWNoZWQubmctcHJpc3RpbmUubmctdmFsaWQge1xuICAgIC8qYmFja2dyb3VuZCBvZiB0aGUgaW5wdXQgYm94Ki9cbiAgICBoZWlnaHQ6IDQ4cHg7XG4gICAgdG9wOiA1JTtcbiAgICBwb3NpdGlvbjogYWJzb2x1dGU7XG59XG5cblxuOjpuZy1kZWVwIC5uZy1zdGFyLWluc2VydGVkIHtcbiAgICBjb2xvcjogI2ZmODQyMCAhaW1wb3J0YW50O1xufVxuIl19 */"

/***/ }),

/***/ "./src/app/map/search-bar/search.component.ts":
/*!****************************************************!*\
  !*** ./src/app/map/search-bar/search.component.ts ***!
  \****************************************************/
/*! exports provided: SearchComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SearchComponent", function() { return SearchComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../services/map-service/map.service */ "./src/app/services/map-service/map.service.ts");
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! leaflet/dist/leaflet.css */ "./node_modules/leaflet/dist/leaflet.css");
/* harmony import */ var leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(leaflet_dist_leaflet_css__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! leaflet-maskcanvas */ "./node_modules/leaflet-maskcanvas/dist/L.GridLayer.MaskCanvas.js");
/* harmony import */ var leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(leaflet_maskcanvas__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _angular_forms__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @angular/forms */ "./node_modules/@angular/forms/fesm2015/forms.js");
/* harmony import */ var _angular_cdk__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @angular/cdk */ "./node_modules/@angular/cdk/esm2015/cdk.js");
/* harmony import */ var _services_search_search_service__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../../services/search/search.service */ "./src/app/services/search/search.service.ts");








let SearchComponent = class SearchComponent {
    constructor(mapService, searchService) {
        this.mapService = mapService;
        this.searchService = searchService;
        this.formControl = new _angular_forms__WEBPACK_IMPORTED_MODULE_5__["FormControl"]();
        this.dropDownHandler = (event) => {
            // clears any possible existing value from search box
            if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp' && event.key !== 'Enter') {
                if (event.target.value !== '') {
                    this.mapService.getDropBox(event.target.value).subscribe(this.getSearchInputDataHandler);
                    // gets auto-completion suggestion from the database
                }
            }
            if (event.key === 'Enter') {
                this.selected(null, event.target.value);
            }
        };
        this.getSearchInputDataHandler = (data) => {
            // process the data, make the display look more aesthetic
            let i;
            let cityString = '';
            let countyString = '';
            let stateString = '';
            this.dataToDropDownMenu = [];
            for (i = 0; i < data.length; i++) {
                // if the level data exists, add to the dictionary arr, then add arr to list dataToDropDownMen
                if (data[i][0]) {
                    cityString = data[i][0] + ', ';
                }
                if (data[i][1]) {
                    countyString = data[i][1] + ', ';
                }
                if (data[i][2]) {
                    stateString = data[i][2];
                }
                // 'value' is for showing on the search box
                const value = cityString + countyString + stateString;
                const id = data[i][3];
                // 'id' is for accurately locating the location
                this.dataToDropDownMenu.push({ display: value, value, id });
            }
        };
        this.userInputCheckHandler = ([[data], value]) => {
            // given the boundary data after the keyword search, fits the map according to the boundary and shows the name label
            if (data) {
            }
            else {
                document.getElementById('search-input-id').value = '';
                document.getElementById('placeholder').innerHTML = 'Please enter again';
            }
        };
        this.selected = (id, value) => {
            // FIXME: county id are all set to 6 due to the lack of county id data
            // passes the id and location name to search component
            if (id) {
                this.searchService.getSearch(id).subscribe((data) => {
                    this.searchService.searchDataLoaded.emit([data, value]);
                });
            }
            else {
                this.searchService.getSearch(value).subscribe((data) => {
                    this.searchService.searchDataLoaded.emit([data, value]);
                });
            }
        };
    }
    ngOnInit() {
        this.searchService.searchDataLoaded.subscribe(this.userInputCheckHandler);
    }
};
SearchComponent.ctorParameters = () => [
    { type: _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_2__["MapService"] },
    { type: _services_search_search_service__WEBPACK_IMPORTED_MODULE_7__["SearchService"] }
];
SearchComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-search-bar',
        template: __webpack_require__(/*! raw-loader!./search.component.html */ "./node_modules/raw-loader/index.js!./src/app/map/search-bar/search.component.html"),
        styles: [__webpack_require__(/*! ./search.component.css */ "./src/app/map/search-bar/search.component.css")]
    })
], SearchComponent);



/***/ }),

/***/ "./src/app/map/sidebar/sidebar.component.css":
/*!***************************************************!*\
  !*** ./src/app/map/sidebar/sidebar.component.css ***!
  \***************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "#sidebar h4 {\n    margin-top: 40px;\n    color: white;\n}\n\n#sidebar p {\n    color: #e25822;\n}\n\n#sidebar {\n    width: 200px;\n    height: 600px;\n    background: rgba(255, 255, 255, 0.7);\n    top: 10%;\n    position: absolute;\n    z-index: 1000;\n    padding: 10px 15px;\n    font: 14px/16px Arial, Helvetica, sans-serif;\n    text-align: center;\n    display: block;\n}\n\n.switch {\n    position: relative;\n    display: inline-block;\n    width: 60px;\n    height: 34px;\n}\n\n/* Hide default HTML checkbox */\n\n.switch input {\n    opacity: 0;\n    width: 0;\n    height: 0;\n}\n\n/* The slider */\n\n.slider {\n    position: absolute;\n    cursor: pointer;\n    top: 0;\n    left: 0;\n    right: 0;\n    bottom: 0;\n    background-color: #ccc;\n    transition: .4s;\n}\n\n.slider:before {\n    position: absolute;\n    content: \"\";\n    height: 26px;\n    width: 26px;\n    left: 4px;\n    bottom: 4px;\n    background-color: white;\n    transition: .4s;\n}\n\ninput:checked + .slider {\n    background-color: #e25822;\n}\n\ninput:focus + .slider {\n    box-shadow: 0 0 1px #e25822;\n}\n\ninput:checked + .slider:before {\n    -webkit-transform: translateX(26px);\n    transform: translateX(26px);\n}\n\n/* Rounded sliders */\n\n.slider.round {\n    border-radius: 34px;\n}\n\n.slider.round:before {\n    border-radius: 50%;\n}\n\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvbWFwL3NpZGViYXIvc2lkZWJhci5jb21wb25lbnQuY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0lBQ0ksZ0JBQWdCO0lBQ2hCLFlBQVk7QUFDaEI7O0FBRUE7SUFDSSxjQUFjO0FBQ2xCOztBQUVBO0lBQ0ksWUFBWTtJQUNaLGFBQWE7SUFDYixvQ0FBb0M7SUFDcEMsUUFBUTtJQUNSLGtCQUFrQjtJQUNsQixhQUFhO0lBQ2Isa0JBQWtCO0lBQ2xCLDRDQUE0QztJQUM1QyxrQkFBa0I7SUFDbEIsY0FBYztBQUNsQjs7QUFHQTtJQUNJLGtCQUFrQjtJQUNsQixxQkFBcUI7SUFDckIsV0FBVztJQUNYLFlBQVk7QUFDaEI7O0FBRUEsK0JBQStCOztBQUMvQjtJQUNJLFVBQVU7SUFDVixRQUFRO0lBQ1IsU0FBUztBQUNiOztBQUVBLGVBQWU7O0FBQ2Y7SUFDSSxrQkFBa0I7SUFDbEIsZUFBZTtJQUNmLE1BQU07SUFDTixPQUFPO0lBQ1AsUUFBUTtJQUNSLFNBQVM7SUFDVCxzQkFBc0I7SUFFdEIsZUFBZTtBQUNuQjs7QUFFQTtJQUNJLGtCQUFrQjtJQUNsQixXQUFXO0lBQ1gsWUFBWTtJQUNaLFdBQVc7SUFDWCxTQUFTO0lBQ1QsV0FBVztJQUNYLHVCQUF1QjtJQUV2QixlQUFlO0FBQ25COztBQUVBO0lBQ0kseUJBQXlCO0FBQzdCOztBQUVBO0lBQ0ksMkJBQTJCO0FBQy9COztBQUVBO0lBQ0ksbUNBQW1DO0lBRW5DLDJCQUEyQjtBQUMvQjs7QUFFQSxvQkFBb0I7O0FBQ3BCO0lBQ0ksbUJBQW1CO0FBQ3ZCOztBQUVBO0lBQ0ksa0JBQWtCO0FBQ3RCIiwiZmlsZSI6InNyYy9hcHAvbWFwL3NpZGViYXIvc2lkZWJhci5jb21wb25lbnQuY3NzIiwic291cmNlc0NvbnRlbnQiOlsiI3NpZGViYXIgaDQge1xuICAgIG1hcmdpbi10b3A6IDQwcHg7XG4gICAgY29sb3I6IHdoaXRlO1xufVxuXG4jc2lkZWJhciBwIHtcbiAgICBjb2xvcjogI2UyNTgyMjtcbn1cblxuI3NpZGViYXIge1xuICAgIHdpZHRoOiAyMDBweDtcbiAgICBoZWlnaHQ6IDYwMHB4O1xuICAgIGJhY2tncm91bmQ6IHJnYmEoMjU1LCAyNTUsIDI1NSwgMC43KTtcbiAgICB0b3A6IDEwJTtcbiAgICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gICAgei1pbmRleDogMTAwMDtcbiAgICBwYWRkaW5nOiAxMHB4IDE1cHg7XG4gICAgZm9udDogMTRweC8xNnB4IEFyaWFsLCBIZWx2ZXRpY2EsIHNhbnMtc2VyaWY7XG4gICAgdGV4dC1hbGlnbjogY2VudGVyO1xuICAgIGRpc3BsYXk6IGJsb2NrO1xufVxuXG5cbi5zd2l0Y2gge1xuICAgIHBvc2l0aW9uOiByZWxhdGl2ZTtcbiAgICBkaXNwbGF5OiBpbmxpbmUtYmxvY2s7XG4gICAgd2lkdGg6IDYwcHg7XG4gICAgaGVpZ2h0OiAzNHB4O1xufVxuXG4vKiBIaWRlIGRlZmF1bHQgSFRNTCBjaGVja2JveCAqL1xuLnN3aXRjaCBpbnB1dCB7XG4gICAgb3BhY2l0eTogMDtcbiAgICB3aWR0aDogMDtcbiAgICBoZWlnaHQ6IDA7XG59XG5cbi8qIFRoZSBzbGlkZXIgKi9cbi5zbGlkZXIge1xuICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbiAgICBjdXJzb3I6IHBvaW50ZXI7XG4gICAgdG9wOiAwO1xuICAgIGxlZnQ6IDA7XG4gICAgcmlnaHQ6IDA7XG4gICAgYm90dG9tOiAwO1xuICAgIGJhY2tncm91bmQtY29sb3I6ICNjY2M7XG4gICAgLXdlYmtpdC10cmFuc2l0aW9uOiAuNHM7XG4gICAgdHJhbnNpdGlvbjogLjRzO1xufVxuXG4uc2xpZGVyOmJlZm9yZSB7XG4gICAgcG9zaXRpb246IGFic29sdXRlO1xuICAgIGNvbnRlbnQ6IFwiXCI7XG4gICAgaGVpZ2h0OiAyNnB4O1xuICAgIHdpZHRoOiAyNnB4O1xuICAgIGxlZnQ6IDRweDtcbiAgICBib3R0b206IDRweDtcbiAgICBiYWNrZ3JvdW5kLWNvbG9yOiB3aGl0ZTtcbiAgICAtd2Via2l0LXRyYW5zaXRpb246IC40cztcbiAgICB0cmFuc2l0aW9uOiAuNHM7XG59XG5cbmlucHV0OmNoZWNrZWQgKyAuc2xpZGVyIHtcbiAgICBiYWNrZ3JvdW5kLWNvbG9yOiAjZTI1ODIyO1xufVxuXG5pbnB1dDpmb2N1cyArIC5zbGlkZXIge1xuICAgIGJveC1zaGFkb3c6IDAgMCAxcHggI2UyNTgyMjtcbn1cblxuaW5wdXQ6Y2hlY2tlZCArIC5zbGlkZXI6YmVmb3JlIHtcbiAgICAtd2Via2l0LXRyYW5zZm9ybTogdHJhbnNsYXRlWCgyNnB4KTtcbiAgICAtbXMtdHJhbnNmb3JtOiB0cmFuc2xhdGVYKDI2cHgpO1xuICAgIHRyYW5zZm9ybTogdHJhbnNsYXRlWCgyNnB4KTtcbn1cblxuLyogUm91bmRlZCBzbGlkZXJzICovXG4uc2xpZGVyLnJvdW5kIHtcbiAgICBib3JkZXItcmFkaXVzOiAzNHB4O1xufVxuXG4uc2xpZGVyLnJvdW5kOmJlZm9yZSB7XG4gICAgYm9yZGVyLXJhZGl1czogNTAlO1xufVxuIl19 */"

/***/ }),

/***/ "./src/app/map/sidebar/sidebar.component.ts":
/*!**************************************************!*\
  !*** ./src/app/map/sidebar/sidebar.component.ts ***!
  \**************************************************/
/*! exports provided: SidebarComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SidebarComponent", function() { return SidebarComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");


let SidebarComponent = class SidebarComponent {
    constructor() {
    }
    ngOnInit() {
    }
};
SidebarComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-sidebar',
        template: __webpack_require__(/*! raw-loader!./sidebar.component.html */ "./node_modules/raw-loader/index.js!./src/app/map/sidebar/sidebar.component.html"),
        styles: [__webpack_require__(/*! ./sidebar.component.css */ "./src/app/map/sidebar/sidebar.component.css")]
    })
], SidebarComponent);



/***/ }),

/***/ "./src/app/map/sidebar/temperature-range-slider/temperature-range-slider.component.css":
/*!*********************************************************************************************!*\
  !*** ./src/app/map/sidebar/temperature-range-slider/temperature-range-slider.component.css ***!
  \*********************************************************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "#wrapper {\n    margin: 20px auto auto;\n    display: flex;\n    flex-direction: column;\n    align-items: center;\n}\n\n#thermometer {\n    width: 12.5px;\n    background: #38383f;\n    height: 120px;\n    position: relative;\n    border: 9px solid #2a2a2e;\n    border-radius: 20px;\n    z-index: 1;\n    margin-bottom: 50px;\n}\n\n#thermometer:before, #thermometer:after {\n    position: absolute;\n    content: \"\";\n    border-radius: 50%;\n}\n\n#thermometer:before {\n    width: 100%;\n    height: 34px;\n    bottom: 9px;\n    background: #38383f;\n    z-index: -1;\n}\n\n#thermometer:after {\n    -webkit-transform: translateX(-50%);\n            transform: translateX(-50%);\n    width: 25px;\n    height: 25px;\n    background-color: #3dcadf;\n    bottom: -41px;\n    border: 9px solid #2a2a2e;\n    z-index: -3;\n    left: 50%;\n}\n\n#thermometer #graduations {\n    height: 59%;\n    top: 20%;\n    width: 50%;\n}\n\n#thermometer #graduations, #thermometer #graduations:before {\n    position: absolute;\n    border-top: 2px solid rgba(0, 0, 0, 0.5);\n    border-bottom: 2px solid rgba(0, 0, 0, 0.5);\n}\n\n#thermometer #graduations:before {\n    content: \"\";\n    height: 34%;\n    width: 100%;\n    top: 32%;\n}\n\n#thermometer #temperature {\n    bottom: 0;\n    background: linear-gradient(#f17a65, #3dcadf) no-repeat bottom;\n    width: 100%;\n    border-radius: 20px;\n    background-size: 100% 240px;\n    transition: all 0.2s ease-in-out;\n}\n\n#thermometer #temperature, #thermometer #temperature:before, #thermometer #temperature:after {\n    position: absolute;\n}\n\n#thermometer #temperature:before {\n    content: attr(data-value);\n    background: rgba(0, 0, 0, 0.7);\n    color: white;\n    z-index: 2;\n    padding: 5px 10px;\n    border-radius: 5px;\n    font-size: 1em;\n    line-height: 1;\n    -webkit-transform: translateY(50%);\n            transform: translateY(50%);\n    left: calc(100% + 1em / 1.5);\n    top: calc(-1em + 5px - 5px * 2);\n}\n\n#thermometer #temperature:after {\n    content: \"\";\n    border-top: 0.4545454545em solid transparent;\n    border-bottom: 0.4545454545em solid transparent;\n    border-right: 0.6666666667em solid rgba(0, 0, 0, 0.7);\n    left: 100%;\n    top: calc(-1em / 2.2 + 5px);\n}\n\n#temperatureSelectForm {\n    font-size: 1.1em;\n}\n\n#temperatureSelectForm .range {\n    display: flex;\n}\n\n#temperatureSelectForm .range input[type=\"text\"] {\n    width: 2em;\n    background: transparent;\n    border: none;\n    color: inherit;\n    font: inherit;\n    margin: 0 5px;\n    padding: 0 5px;\n    border-bottom: 2px solid transparent;\n    transition: all 0.2s ease-in-out;\n}\n\n#temperatureSelectForm .range input[type=\"text\"]:focus {\n    border-color: #3dcadf;\n    outline: none;\n}\n\n#temperatureSelectForm .range input[type=\"text\"]:first-child {\n    text-align: right;\n}\n\n#temperatureSelectForm .unit {\n    width: 100%;\n    margin: 0;\n    text-align: center;\n}\n\n#temperatureSelectForm .range .tempLabel {\n    width: 50px\n}\n\n#temperatureSelectForm .unit:hover {\n    cursor: pointer;\n}\n\n.tempselect {\n    -webkit-appearance: none;\n    background: transparent;\n    margin: 6px 0;\n    width: 100%;\n}\n\n.tempselect::-moz-focus-outer {\n    border: 0;\n}\n\n.tempselect:hover {\n    cursor: pointer;\n}\n\n.tempselect:focus {\n    outline: 0;\n}\n\n.tempselect:focus::-webkit-slider-runnable-track {\n    background: #313137;\n    border-color: #313137;\n}\n\n.tempselect:focus::-ms-fill-lower {\n    background: #2a2a2e;\n}\n\n.tempselect:focus::-ms-fill-upper {\n    background: #313137;\n    border-color: #313137;\n}\n\n.tempselect::-webkit-slider-runnable-track {\n    height: 10px;\n    width: 100%;\n    cursor: pointer;\n    transition: all 0.2s ease-in-out;\n    box-shadow: 1px 1px 1px transparent, 0 0 1px rgba(13, 13, 13, 0);\n    background: #2a2a2e;\n    border: 2px solid #2a2a2e;\n    border-radius: 5px;\n}\n\n.tempselect::-webkit-slider-thumb {\n    box-shadow: 4px 4px 4px transparent, 0 0 4px rgba(13, 13, 13, 0);\n    background: #3dcadf;\n    border: 0 solid #3d3d44;\n    border-radius: 12px;\n    cursor: pointer;\n    height: 11px;\n    width: 18px;\n    -webkit-appearance: none;\n    margin-top: -2.5px;\n}\n\n.tempselect::-moz-range-track {\n    box-shadow: 1px 1px 1px transparent, 0 0 1px rgba(13, 13, 13, 0);\n    width: 100%;\n    cursor: pointer;\n    transition: all 0.2s ease-in-out;\n    background: #2a2a2e;\n    border: 2px solid #2a2a2e;\n    border-radius: 5px;\n    height: 5px;\n}\n\n.tempselect::-moz-range-thumb {\n    box-shadow: 4px 4px 4px transparent, 0 0 4px rgba(13, 13, 13, 0);\n    background: #3dcadf;\n    border: 0 solid #3d3d44;\n    border-radius: 12px;\n    cursor: pointer;\n    height: 7px;\n    width: 14px;\n}\n\n.tempselect::-ms-track {\n    height: 10px;\n    width: 100%;\n    cursor: pointer;\n    transition: all 0.2s ease-in-out;\n    background: transparent;\n    border-color: transparent;\n    border-width: 5.5px 0;\n    color: transparent;\n}\n\n.tempselect::-ms-fill-lower {\n    box-shadow: 1px 1px 1px transparent, 0 0 1px rgba(13, 13, 13, 0);\n    background: #222226;\n    border: 2px solid #2a2a2e;\n    border-radius: 10px;\n}\n\n.tempselect::-ms-fill-upper {\n    box-shadow: 1px 1px 1px transparent, 0 0 1px rgba(13, 13, 13, 0);\n    background: #2a2a2e;\n    border: 2px solid #2a2a2e;\n    border-radius: 10px;\n}\n\n.tempselect::-ms-thumb {\n    box-shadow: 4px 4px 4px transparent, 0 0 4px rgba(13, 13, 13, 0);\n    background: #3dcadf;\n    border: 0 solid #3d3d44;\n    border-radius: 12px;\n    cursor: pointer;\n    height: 7px;\n    width: 14px;\n    margin-top: 3px;\n}\n\n.tempselect:disabled::-webkit-slider-thumb {\n    cursor: not-allowed;\n}\n\n.tempselect:disabled::-moz-range-thumb {\n    cursor: not-allowed;\n}\n\n.tempselect:disabled::-ms-thumb {\n    cursor: not-allowed;\n}\n\n.tempselect:disabled::-webkit-slider-runnable-track {\n    cursor: not-allowed;\n}\n\n.tempselect:disabled::-ms-fill-lower {\n    cursor: not-allowed;\n}\n\n.tempselect:disabled::-ms-fill-upper {\n    cursor: not-allowed;\n}\n\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvbWFwL3NpZGViYXIvdGVtcGVyYXR1cmUtcmFuZ2Utc2xpZGVyL3RlbXBlcmF0dXJlLXJhbmdlLXNsaWRlci5jb21wb25lbnQuY3NzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0lBQ0ksc0JBQXNCO0lBQ3RCLGFBQWE7SUFDYixzQkFBc0I7SUFDdEIsbUJBQW1CO0FBQ3ZCOztBQUVBO0lBQ0ksYUFBYTtJQUNiLG1CQUFtQjtJQUNuQixhQUFhO0lBQ2Isa0JBQWtCO0lBQ2xCLHlCQUF5QjtJQUN6QixtQkFBbUI7SUFDbkIsVUFBVTtJQUNWLG1CQUFtQjtBQUN2Qjs7QUFFQTtJQUNJLGtCQUFrQjtJQUNsQixXQUFXO0lBQ1gsa0JBQWtCO0FBQ3RCOztBQUVBO0lBQ0ksV0FBVztJQUNYLFlBQVk7SUFDWixXQUFXO0lBQ1gsbUJBQW1CO0lBQ25CLFdBQVc7QUFDZjs7QUFFQTtJQUNJLG1DQUEyQjtZQUEzQiwyQkFBMkI7SUFDM0IsV0FBVztJQUNYLFlBQVk7SUFDWix5QkFBeUI7SUFDekIsYUFBYTtJQUNiLHlCQUF5QjtJQUN6QixXQUFXO0lBQ1gsU0FBUztBQUNiOztBQUVBO0lBQ0ksV0FBVztJQUNYLFFBQVE7SUFDUixVQUFVO0FBQ2Q7O0FBRUE7SUFDSSxrQkFBa0I7SUFDbEIsd0NBQXdDO0lBQ3hDLDJDQUEyQztBQUMvQzs7QUFFQTtJQUNJLFdBQVc7SUFDWCxXQUFXO0lBQ1gsV0FBVztJQUNYLFFBQVE7QUFDWjs7QUFFQTtJQUNJLFNBQVM7SUFDVCw4REFBOEQ7SUFDOUQsV0FBVztJQUNYLG1CQUFtQjtJQUNuQiwyQkFBMkI7SUFDM0IsZ0NBQWdDO0FBQ3BDOztBQUVBO0lBQ0ksa0JBQWtCO0FBQ3RCOztBQUVBO0lBQ0kseUJBQXlCO0lBQ3pCLDhCQUE4QjtJQUM5QixZQUFZO0lBQ1osVUFBVTtJQUNWLGlCQUFpQjtJQUNqQixrQkFBa0I7SUFDbEIsY0FBYztJQUNkLGNBQWM7SUFDZCxrQ0FBMEI7WUFBMUIsMEJBQTBCO0lBQzFCLDRCQUE0QjtJQUM1QiwrQkFBK0I7QUFDbkM7O0FBRUE7SUFDSSxXQUFXO0lBQ1gsNENBQTRDO0lBQzVDLCtDQUErQztJQUMvQyxxREFBcUQ7SUFDckQsVUFBVTtJQUNWLDJCQUEyQjtBQUMvQjs7QUFFQTtJQUNJLGdCQUFnQjtBQUNwQjs7QUFFQTtJQUNJLGFBQWE7QUFDakI7O0FBRUE7SUFDSSxVQUFVO0lBQ1YsdUJBQXVCO0lBQ3ZCLFlBQVk7SUFDWixjQUFjO0lBQ2QsYUFBYTtJQUNiLGFBQWE7SUFDYixjQUFjO0lBQ2Qsb0NBQW9DO0lBQ3BDLGdDQUFnQztBQUNwQzs7QUFFQTtJQUNJLHFCQUFxQjtJQUNyQixhQUFhO0FBQ2pCOztBQUVBO0lBQ0ksaUJBQWlCO0FBQ3JCOztBQUVBO0lBQ0ksV0FBVztJQUNYLFNBQVM7SUFDVCxrQkFBa0I7QUFDdEI7O0FBRUE7SUFDSTtBQUNKOztBQUVBO0lBQ0ksZUFBZTtBQUNuQjs7QUFFQTtJQUNJLHdCQUF3QjtJQUN4Qix1QkFBdUI7SUFDdkIsYUFBYTtJQUNiLFdBQVc7QUFDZjs7QUFFQTtJQUNJLFNBQVM7QUFDYjs7QUFFQTtJQUNJLGVBQWU7QUFDbkI7O0FBRUE7SUFDSSxVQUFVO0FBQ2Q7O0FBRUE7SUFDSSxtQkFBbUI7SUFDbkIscUJBQXFCO0FBQ3pCOztBQUVBO0lBQ0ksbUJBQW1CO0FBQ3ZCOztBQUVBO0lBQ0ksbUJBQW1CO0lBQ25CLHFCQUFxQjtBQUN6Qjs7QUFFQTtJQUNJLFlBQVk7SUFDWixXQUFXO0lBQ1gsZUFBZTtJQUNmLGdDQUFnQztJQUNoQyxnRUFBZ0U7SUFDaEUsbUJBQW1CO0lBQ25CLHlCQUF5QjtJQUN6QixrQkFBa0I7QUFDdEI7O0FBRUE7SUFDSSxnRUFBZ0U7SUFDaEUsbUJBQW1CO0lBQ25CLHVCQUF1QjtJQUN2QixtQkFBbUI7SUFDbkIsZUFBZTtJQUNmLFlBQVk7SUFDWixXQUFXO0lBQ1gsd0JBQXdCO0lBQ3hCLGtCQUFrQjtBQUN0Qjs7QUFFQTtJQUNJLGdFQUFnRTtJQUNoRSxXQUFXO0lBQ1gsZUFBZTtJQUNmLGdDQUFnQztJQUNoQyxtQkFBbUI7SUFDbkIseUJBQXlCO0lBQ3pCLGtCQUFrQjtJQUNsQixXQUFXO0FBQ2Y7O0FBRUE7SUFDSSxnRUFBZ0U7SUFDaEUsbUJBQW1CO0lBQ25CLHVCQUF1QjtJQUN2QixtQkFBbUI7SUFDbkIsZUFBZTtJQUNmLFdBQVc7SUFDWCxXQUFXO0FBQ2Y7O0FBRUE7SUFDSSxZQUFZO0lBQ1osV0FBVztJQUNYLGVBQWU7SUFDZixnQ0FBZ0M7SUFDaEMsdUJBQXVCO0lBQ3ZCLHlCQUF5QjtJQUN6QixxQkFBcUI7SUFDckIsa0JBQWtCO0FBQ3RCOztBQUVBO0lBQ0ksZ0VBQWdFO0lBQ2hFLG1CQUFtQjtJQUNuQix5QkFBeUI7SUFDekIsbUJBQW1CO0FBQ3ZCOztBQUVBO0lBQ0ksZ0VBQWdFO0lBQ2hFLG1CQUFtQjtJQUNuQix5QkFBeUI7SUFDekIsbUJBQW1CO0FBQ3ZCOztBQUVBO0lBQ0ksZ0VBQWdFO0lBQ2hFLG1CQUFtQjtJQUNuQix1QkFBdUI7SUFDdkIsbUJBQW1CO0lBQ25CLGVBQWU7SUFDZixXQUFXO0lBQ1gsV0FBVztJQUNYLGVBQWU7QUFDbkI7O0FBRUE7SUFDSSxtQkFBbUI7QUFDdkI7O0FBRUE7SUFDSSxtQkFBbUI7QUFDdkI7O0FBRUE7SUFDSSxtQkFBbUI7QUFDdkI7O0FBRUE7SUFDSSxtQkFBbUI7QUFDdkI7O0FBRUE7SUFDSSxtQkFBbUI7QUFDdkI7O0FBRUE7SUFDSSxtQkFBbUI7QUFDdkIiLCJmaWxlIjoic3JjL2FwcC9tYXAvc2lkZWJhci90ZW1wZXJhdHVyZS1yYW5nZS1zbGlkZXIvdGVtcGVyYXR1cmUtcmFuZ2Utc2xpZGVyLmNvbXBvbmVudC5jc3MiLCJzb3VyY2VzQ29udGVudCI6WyIjd3JhcHBlciB7XG4gICAgbWFyZ2luOiAyMHB4IGF1dG8gYXV0bztcbiAgICBkaXNwbGF5OiBmbGV4O1xuICAgIGZsZXgtZGlyZWN0aW9uOiBjb2x1bW47XG4gICAgYWxpZ24taXRlbXM6IGNlbnRlcjtcbn1cblxuI3RoZXJtb21ldGVyIHtcbiAgICB3aWR0aDogMTIuNXB4O1xuICAgIGJhY2tncm91bmQ6ICMzODM4M2Y7XG4gICAgaGVpZ2h0OiAxMjBweDtcbiAgICBwb3NpdGlvbjogcmVsYXRpdmU7XG4gICAgYm9yZGVyOiA5cHggc29saWQgIzJhMmEyZTtcbiAgICBib3JkZXItcmFkaXVzOiAyMHB4O1xuICAgIHotaW5kZXg6IDE7XG4gICAgbWFyZ2luLWJvdHRvbTogNTBweDtcbn1cblxuI3RoZXJtb21ldGVyOmJlZm9yZSwgI3RoZXJtb21ldGVyOmFmdGVyIHtcbiAgICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gICAgY29udGVudDogXCJcIjtcbiAgICBib3JkZXItcmFkaXVzOiA1MCU7XG59XG5cbiN0aGVybW9tZXRlcjpiZWZvcmUge1xuICAgIHdpZHRoOiAxMDAlO1xuICAgIGhlaWdodDogMzRweDtcbiAgICBib3R0b206IDlweDtcbiAgICBiYWNrZ3JvdW5kOiAjMzgzODNmO1xuICAgIHotaW5kZXg6IC0xO1xufVxuXG4jdGhlcm1vbWV0ZXI6YWZ0ZXIge1xuICAgIHRyYW5zZm9ybTogdHJhbnNsYXRlWCgtNTAlKTtcbiAgICB3aWR0aDogMjVweDtcbiAgICBoZWlnaHQ6IDI1cHg7XG4gICAgYmFja2dyb3VuZC1jb2xvcjogIzNkY2FkZjtcbiAgICBib3R0b206IC00MXB4O1xuICAgIGJvcmRlcjogOXB4IHNvbGlkICMyYTJhMmU7XG4gICAgei1pbmRleDogLTM7XG4gICAgbGVmdDogNTAlO1xufVxuXG4jdGhlcm1vbWV0ZXIgI2dyYWR1YXRpb25zIHtcbiAgICBoZWlnaHQ6IDU5JTtcbiAgICB0b3A6IDIwJTtcbiAgICB3aWR0aDogNTAlO1xufVxuXG4jdGhlcm1vbWV0ZXIgI2dyYWR1YXRpb25zLCAjdGhlcm1vbWV0ZXIgI2dyYWR1YXRpb25zOmJlZm9yZSB7XG4gICAgcG9zaXRpb246IGFic29sdXRlO1xuICAgIGJvcmRlci10b3A6IDJweCBzb2xpZCByZ2JhKDAsIDAsIDAsIDAuNSk7XG4gICAgYm9yZGVyLWJvdHRvbTogMnB4IHNvbGlkIHJnYmEoMCwgMCwgMCwgMC41KTtcbn1cblxuI3RoZXJtb21ldGVyICNncmFkdWF0aW9uczpiZWZvcmUge1xuICAgIGNvbnRlbnQ6IFwiXCI7XG4gICAgaGVpZ2h0OiAzNCU7XG4gICAgd2lkdGg6IDEwMCU7XG4gICAgdG9wOiAzMiU7XG59XG5cbiN0aGVybW9tZXRlciAjdGVtcGVyYXR1cmUge1xuICAgIGJvdHRvbTogMDtcbiAgICBiYWNrZ3JvdW5kOiBsaW5lYXItZ3JhZGllbnQoI2YxN2E2NSwgIzNkY2FkZikgbm8tcmVwZWF0IGJvdHRvbTtcbiAgICB3aWR0aDogMTAwJTtcbiAgICBib3JkZXItcmFkaXVzOiAyMHB4O1xuICAgIGJhY2tncm91bmQtc2l6ZTogMTAwJSAyNDBweDtcbiAgICB0cmFuc2l0aW9uOiBhbGwgMC4ycyBlYXNlLWluLW91dDtcbn1cblxuI3RoZXJtb21ldGVyICN0ZW1wZXJhdHVyZSwgI3RoZXJtb21ldGVyICN0ZW1wZXJhdHVyZTpiZWZvcmUsICN0aGVybW9tZXRlciAjdGVtcGVyYXR1cmU6YWZ0ZXIge1xuICAgIHBvc2l0aW9uOiBhYnNvbHV0ZTtcbn1cblxuI3RoZXJtb21ldGVyICN0ZW1wZXJhdHVyZTpiZWZvcmUge1xuICAgIGNvbnRlbnQ6IGF0dHIoZGF0YS12YWx1ZSk7XG4gICAgYmFja2dyb3VuZDogcmdiYSgwLCAwLCAwLCAwLjcpO1xuICAgIGNvbG9yOiB3aGl0ZTtcbiAgICB6LWluZGV4OiAyO1xuICAgIHBhZGRpbmc6IDVweCAxMHB4O1xuICAgIGJvcmRlci1yYWRpdXM6IDVweDtcbiAgICBmb250LXNpemU6IDFlbTtcbiAgICBsaW5lLWhlaWdodDogMTtcbiAgICB0cmFuc2Zvcm06IHRyYW5zbGF0ZVkoNTAlKTtcbiAgICBsZWZ0OiBjYWxjKDEwMCUgKyAxZW0gLyAxLjUpO1xuICAgIHRvcDogY2FsYygtMWVtICsgNXB4IC0gNXB4ICogMik7XG59XG5cbiN0aGVybW9tZXRlciAjdGVtcGVyYXR1cmU6YWZ0ZXIge1xuICAgIGNvbnRlbnQ6IFwiXCI7XG4gICAgYm9yZGVyLXRvcDogMC40NTQ1NDU0NTQ1ZW0gc29saWQgdHJhbnNwYXJlbnQ7XG4gICAgYm9yZGVyLWJvdHRvbTogMC40NTQ1NDU0NTQ1ZW0gc29saWQgdHJhbnNwYXJlbnQ7XG4gICAgYm9yZGVyLXJpZ2h0OiAwLjY2NjY2NjY2NjdlbSBzb2xpZCByZ2JhKDAsIDAsIDAsIDAuNyk7XG4gICAgbGVmdDogMTAwJTtcbiAgICB0b3A6IGNhbGMoLTFlbSAvIDIuMiArIDVweCk7XG59XG5cbiN0ZW1wZXJhdHVyZVNlbGVjdEZvcm0ge1xuICAgIGZvbnQtc2l6ZTogMS4xZW07XG59XG5cbiN0ZW1wZXJhdHVyZVNlbGVjdEZvcm0gLnJhbmdlIHtcbiAgICBkaXNwbGF5OiBmbGV4O1xufVxuXG4jdGVtcGVyYXR1cmVTZWxlY3RGb3JtIC5yYW5nZSBpbnB1dFt0eXBlPVwidGV4dFwiXSB7XG4gICAgd2lkdGg6IDJlbTtcbiAgICBiYWNrZ3JvdW5kOiB0cmFuc3BhcmVudDtcbiAgICBib3JkZXI6IG5vbmU7XG4gICAgY29sb3I6IGluaGVyaXQ7XG4gICAgZm9udDogaW5oZXJpdDtcbiAgICBtYXJnaW46IDAgNXB4O1xuICAgIHBhZGRpbmc6IDAgNXB4O1xuICAgIGJvcmRlci1ib3R0b206IDJweCBzb2xpZCB0cmFuc3BhcmVudDtcbiAgICB0cmFuc2l0aW9uOiBhbGwgMC4ycyBlYXNlLWluLW91dDtcbn1cblxuI3RlbXBlcmF0dXJlU2VsZWN0Rm9ybSAucmFuZ2UgaW5wdXRbdHlwZT1cInRleHRcIl06Zm9jdXMge1xuICAgIGJvcmRlci1jb2xvcjogIzNkY2FkZjtcbiAgICBvdXRsaW5lOiBub25lO1xufVxuXG4jdGVtcGVyYXR1cmVTZWxlY3RGb3JtIC5yYW5nZSBpbnB1dFt0eXBlPVwidGV4dFwiXTpmaXJzdC1jaGlsZCB7XG4gICAgdGV4dC1hbGlnbjogcmlnaHQ7XG59XG5cbiN0ZW1wZXJhdHVyZVNlbGVjdEZvcm0gLnVuaXQge1xuICAgIHdpZHRoOiAxMDAlO1xuICAgIG1hcmdpbjogMDtcbiAgICB0ZXh0LWFsaWduOiBjZW50ZXI7XG59XG5cbiN0ZW1wZXJhdHVyZVNlbGVjdEZvcm0gLnJhbmdlIC50ZW1wTGFiZWwge1xuICAgIHdpZHRoOiA1MHB4XG59XG5cbiN0ZW1wZXJhdHVyZVNlbGVjdEZvcm0gLnVuaXQ6aG92ZXIge1xuICAgIGN1cnNvcjogcG9pbnRlcjtcbn1cblxuLnRlbXBzZWxlY3Qge1xuICAgIC13ZWJraXQtYXBwZWFyYW5jZTogbm9uZTtcbiAgICBiYWNrZ3JvdW5kOiB0cmFuc3BhcmVudDtcbiAgICBtYXJnaW46IDZweCAwO1xuICAgIHdpZHRoOiAxMDAlO1xufVxuXG4udGVtcHNlbGVjdDo6LW1vei1mb2N1cy1vdXRlciB7XG4gICAgYm9yZGVyOiAwO1xufVxuXG4udGVtcHNlbGVjdDpob3ZlciB7XG4gICAgY3Vyc29yOiBwb2ludGVyO1xufVxuXG4udGVtcHNlbGVjdDpmb2N1cyB7XG4gICAgb3V0bGluZTogMDtcbn1cblxuLnRlbXBzZWxlY3Q6Zm9jdXM6Oi13ZWJraXQtc2xpZGVyLXJ1bm5hYmxlLXRyYWNrIHtcbiAgICBiYWNrZ3JvdW5kOiAjMzEzMTM3O1xuICAgIGJvcmRlci1jb2xvcjogIzMxMzEzNztcbn1cblxuLnRlbXBzZWxlY3Q6Zm9jdXM6Oi1tcy1maWxsLWxvd2VyIHtcbiAgICBiYWNrZ3JvdW5kOiAjMmEyYTJlO1xufVxuXG4udGVtcHNlbGVjdDpmb2N1czo6LW1zLWZpbGwtdXBwZXIge1xuICAgIGJhY2tncm91bmQ6ICMzMTMxMzc7XG4gICAgYm9yZGVyLWNvbG9yOiAjMzEzMTM3O1xufVxuXG4udGVtcHNlbGVjdDo6LXdlYmtpdC1zbGlkZXItcnVubmFibGUtdHJhY2sge1xuICAgIGhlaWdodDogMTBweDtcbiAgICB3aWR0aDogMTAwJTtcbiAgICBjdXJzb3I6IHBvaW50ZXI7XG4gICAgdHJhbnNpdGlvbjogYWxsIDAuMnMgZWFzZS1pbi1vdXQ7XG4gICAgYm94LXNoYWRvdzogMXB4IDFweCAxcHggdHJhbnNwYXJlbnQsIDAgMCAxcHggcmdiYSgxMywgMTMsIDEzLCAwKTtcbiAgICBiYWNrZ3JvdW5kOiAjMmEyYTJlO1xuICAgIGJvcmRlcjogMnB4IHNvbGlkICMyYTJhMmU7XG4gICAgYm9yZGVyLXJhZGl1czogNXB4O1xufVxuXG4udGVtcHNlbGVjdDo6LXdlYmtpdC1zbGlkZXItdGh1bWIge1xuICAgIGJveC1zaGFkb3c6IDRweCA0cHggNHB4IHRyYW5zcGFyZW50LCAwIDAgNHB4IHJnYmEoMTMsIDEzLCAxMywgMCk7XG4gICAgYmFja2dyb3VuZDogIzNkY2FkZjtcbiAgICBib3JkZXI6IDAgc29saWQgIzNkM2Q0NDtcbiAgICBib3JkZXItcmFkaXVzOiAxMnB4O1xuICAgIGN1cnNvcjogcG9pbnRlcjtcbiAgICBoZWlnaHQ6IDExcHg7XG4gICAgd2lkdGg6IDE4cHg7XG4gICAgLXdlYmtpdC1hcHBlYXJhbmNlOiBub25lO1xuICAgIG1hcmdpbi10b3A6IC0yLjVweDtcbn1cblxuLnRlbXBzZWxlY3Q6Oi1tb3otcmFuZ2UtdHJhY2sge1xuICAgIGJveC1zaGFkb3c6IDFweCAxcHggMXB4IHRyYW5zcGFyZW50LCAwIDAgMXB4IHJnYmEoMTMsIDEzLCAxMywgMCk7XG4gICAgd2lkdGg6IDEwMCU7XG4gICAgY3Vyc29yOiBwb2ludGVyO1xuICAgIHRyYW5zaXRpb246IGFsbCAwLjJzIGVhc2UtaW4tb3V0O1xuICAgIGJhY2tncm91bmQ6ICMyYTJhMmU7XG4gICAgYm9yZGVyOiAycHggc29saWQgIzJhMmEyZTtcbiAgICBib3JkZXItcmFkaXVzOiA1cHg7XG4gICAgaGVpZ2h0OiA1cHg7XG59XG5cbi50ZW1wc2VsZWN0OjotbW96LXJhbmdlLXRodW1iIHtcbiAgICBib3gtc2hhZG93OiA0cHggNHB4IDRweCB0cmFuc3BhcmVudCwgMCAwIDRweCByZ2JhKDEzLCAxMywgMTMsIDApO1xuICAgIGJhY2tncm91bmQ6ICMzZGNhZGY7XG4gICAgYm9yZGVyOiAwIHNvbGlkICMzZDNkNDQ7XG4gICAgYm9yZGVyLXJhZGl1czogMTJweDtcbiAgICBjdXJzb3I6IHBvaW50ZXI7XG4gICAgaGVpZ2h0OiA3cHg7XG4gICAgd2lkdGg6IDE0cHg7XG59XG5cbi50ZW1wc2VsZWN0OjotbXMtdHJhY2sge1xuICAgIGhlaWdodDogMTBweDtcbiAgICB3aWR0aDogMTAwJTtcbiAgICBjdXJzb3I6IHBvaW50ZXI7XG4gICAgdHJhbnNpdGlvbjogYWxsIDAuMnMgZWFzZS1pbi1vdXQ7XG4gICAgYmFja2dyb3VuZDogdHJhbnNwYXJlbnQ7XG4gICAgYm9yZGVyLWNvbG9yOiB0cmFuc3BhcmVudDtcbiAgICBib3JkZXItd2lkdGg6IDUuNXB4IDA7XG4gICAgY29sb3I6IHRyYW5zcGFyZW50O1xufVxuXG4udGVtcHNlbGVjdDo6LW1zLWZpbGwtbG93ZXIge1xuICAgIGJveC1zaGFkb3c6IDFweCAxcHggMXB4IHRyYW5zcGFyZW50LCAwIDAgMXB4IHJnYmEoMTMsIDEzLCAxMywgMCk7XG4gICAgYmFja2dyb3VuZDogIzIyMjIyNjtcbiAgICBib3JkZXI6IDJweCBzb2xpZCAjMmEyYTJlO1xuICAgIGJvcmRlci1yYWRpdXM6IDEwcHg7XG59XG5cbi50ZW1wc2VsZWN0OjotbXMtZmlsbC11cHBlciB7XG4gICAgYm94LXNoYWRvdzogMXB4IDFweCAxcHggdHJhbnNwYXJlbnQsIDAgMCAxcHggcmdiYSgxMywgMTMsIDEzLCAwKTtcbiAgICBiYWNrZ3JvdW5kOiAjMmEyYTJlO1xuICAgIGJvcmRlcjogMnB4IHNvbGlkICMyYTJhMmU7XG4gICAgYm9yZGVyLXJhZGl1czogMTBweDtcbn1cblxuLnRlbXBzZWxlY3Q6Oi1tcy10aHVtYiB7XG4gICAgYm94LXNoYWRvdzogNHB4IDRweCA0cHggdHJhbnNwYXJlbnQsIDAgMCA0cHggcmdiYSgxMywgMTMsIDEzLCAwKTtcbiAgICBiYWNrZ3JvdW5kOiAjM2RjYWRmO1xuICAgIGJvcmRlcjogMCBzb2xpZCAjM2QzZDQ0O1xuICAgIGJvcmRlci1yYWRpdXM6IDEycHg7XG4gICAgY3Vyc29yOiBwb2ludGVyO1xuICAgIGhlaWdodDogN3B4O1xuICAgIHdpZHRoOiAxNHB4O1xuICAgIG1hcmdpbi10b3A6IDNweDtcbn1cblxuLnRlbXBzZWxlY3Q6ZGlzYWJsZWQ6Oi13ZWJraXQtc2xpZGVyLXRodW1iIHtcbiAgICBjdXJzb3I6IG5vdC1hbGxvd2VkO1xufVxuXG4udGVtcHNlbGVjdDpkaXNhYmxlZDo6LW1vei1yYW5nZS10aHVtYiB7XG4gICAgY3Vyc29yOiBub3QtYWxsb3dlZDtcbn1cblxuLnRlbXBzZWxlY3Q6ZGlzYWJsZWQ6Oi1tcy10aHVtYiB7XG4gICAgY3Vyc29yOiBub3QtYWxsb3dlZDtcbn1cblxuLnRlbXBzZWxlY3Q6ZGlzYWJsZWQ6Oi13ZWJraXQtc2xpZGVyLXJ1bm5hYmxlLXRyYWNrIHtcbiAgICBjdXJzb3I6IG5vdC1hbGxvd2VkO1xufVxuXG4udGVtcHNlbGVjdDpkaXNhYmxlZDo6LW1zLWZpbGwtbG93ZXIge1xuICAgIGN1cnNvcjogbm90LWFsbG93ZWQ7XG59XG5cbi50ZW1wc2VsZWN0OmRpc2FibGVkOjotbXMtZmlsbC11cHBlciB7XG4gICAgY3Vyc29yOiBub3QtYWxsb3dlZDtcbn1cbiJdfQ== */"

/***/ }),

/***/ "./src/app/map/sidebar/temperature-range-slider/temperature-range-slider.component.ts":
/*!********************************************************************************************!*\
  !*** ./src/app/map/sidebar/temperature-range-slider/temperature-range-slider.component.ts ***!
  \********************************************************************************************/
/*! exports provided: TemperatureRangeSliderComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TemperatureRangeSliderComponent", function() { return TemperatureRangeSliderComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ../../../services/map-service/map.service */ "./src/app/services/map-service/map.service.ts");



let TemperatureRangeSliderComponent = class TemperatureRangeSliderComponent {
    constructor(mapService) {
        this.mapService = mapService;
        this.units = {
            Celsius: '°C',
            Fahrenheit: '°F'
        };
        this.config = {
            minTemp: -6,
            maxTemp: 35,
            unit: 'Celsius'
        };
        this.setTemperature = (newValue) => {
            const temperature = document.getElementById('temperature');
            temperature.style.height = (newValue - this.config.minTemp) / (this.config.maxTemp - this.config.minTemp) * 100 + '%';
            temperature.dataset.value = newValue + this.units[this.config.unit];
        };
        this.highTemperatureSelectorUpdate = (event) => {
            const newValue = event.target.value;
            this.setTemperature(newValue);
            this.mapService.temperatureChangeEvent.emit({ high: Number(newValue) });
        };
        this.lowTemperatureSelectorUpdate = (event) => {
            const newValue = event.target.value;
            this.setTemperature(newValue);
            this.mapService.temperatureChangeEvent.emit({ low: Number(newValue) });
        };
    }
    ngOnInit() {
    }
};
TemperatureRangeSliderComponent.ctorParameters = () => [
    { type: _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_2__["MapService"] }
];
TemperatureRangeSliderComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-temperature-range-slider',
        template: __webpack_require__(/*! raw-loader!./temperature-range-slider.component.html */ "./node_modules/raw-loader/index.js!./src/app/map/sidebar/temperature-range-slider/temperature-range-slider.component.html"),
        styles: [__webpack_require__(/*! ./temperature-range-slider.component.css */ "./src/app/map/sidebar/temperature-range-slider/temperature-range-slider.component.css")]
    })
], TemperatureRangeSliderComponent);



/***/ }),

/***/ "./src/app/map/tab/tab.component.css":
/*!*******************************************!*\
  !*** ./src/app/map/tab/tab.component.css ***!
  \*******************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = ".mat-tab-group .mat-tab {\n    position: absolute;\n    z-index: 1000;\n    top: 0;\n}\n\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvbWFwL3RhYi90YWIuY29tcG9uZW50LmNzcyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiQUFBQTtJQUNJLGtCQUFrQjtJQUNsQixhQUFhO0lBQ2IsTUFBTTtBQUNWIiwiZmlsZSI6InNyYy9hcHAvbWFwL3RhYi90YWIuY29tcG9uZW50LmNzcyIsInNvdXJjZXNDb250ZW50IjpbIi5tYXQtdGFiLWdyb3VwIC5tYXQtdGFiIHtcbiAgICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gICAgei1pbmRleDogMTAwMDtcbiAgICB0b3A6IDA7XG59XG4iXX0= */"

/***/ }),

/***/ "./src/app/map/tab/tab.component.ts":
/*!******************************************!*\
  !*** ./src/app/map/tab/tab.component.ts ***!
  \******************************************/
/*! exports provided: TabGroupComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TabGroupComponent", function() { return TabGroupComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");

/**
 * @author Yuan Fu <yuanf9@uci.edu>
 */

let TabGroupComponent = class TabGroupComponent {
    constructor() {
    }
    ngOnInit() {
    }
};
TabGroupComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'tab-group-basic',
        template: __webpack_require__(/*! raw-loader!./tab.component.html */ "./node_modules/raw-loader/index.js!./src/app/map/tab/tab.component.html"),
        styles: [__webpack_require__(/*! ./tab.component.css */ "./src/app/map/tab/tab.component.css")]
    })
], TabGroupComponent);



/***/ }),

/***/ "./src/app/map/time-series/time-series.component.css":
/*!***********************************************************!*\
  !*** ./src/app/map/time-series/time-series.component.css ***!
  \***********************************************************/
/*! no static exports found */
/***/ (function(module, exports) {

module.exports = "#timebar-container {\n  z-index: 1000;\n  position: absolute;\n  bottom: 1%;\n  left: 20%;\n  width: 60%;\n  /*height: 20%;*/\n}\n\n#report {\n  z-index: 1001;\n  position: absolute;\n  bottom: 0;\n  font: 0.8em sans-serif;\n  color: wheat;\n  text-align: center;\n  width: 60%;\n  left: 20%;\n}\n/*# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbInNyYy9hcHAvbWFwL3RpbWUtc2VyaWVzL3RpbWUtc2VyaWVzLmNvbXBvbmVudC5jc3MiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6IkFBQUE7RUFDRSxhQUFhO0VBQ2Isa0JBQWtCO0VBQ2xCLFVBQVU7RUFDVixTQUFTO0VBQ1QsVUFBVTtFQUNWLGVBQWU7QUFDakI7O0FBRUE7RUFDRSxhQUFhO0VBQ2Isa0JBQWtCO0VBQ2xCLFNBQVM7RUFDVCxzQkFBc0I7RUFDdEIsWUFBWTtFQUNaLGtCQUFrQjtFQUNsQixVQUFVO0VBQ1YsU0FBUztBQUNYIiwiZmlsZSI6InNyYy9hcHAvbWFwL3RpbWUtc2VyaWVzL3RpbWUtc2VyaWVzLmNvbXBvbmVudC5jc3MiLCJzb3VyY2VzQ29udGVudCI6WyIjdGltZWJhci1jb250YWluZXIge1xuICB6LWluZGV4OiAxMDAwO1xuICBwb3NpdGlvbjogYWJzb2x1dGU7XG4gIGJvdHRvbTogMSU7XG4gIGxlZnQ6IDIwJTtcbiAgd2lkdGg6IDYwJTtcbiAgLypoZWlnaHQ6IDIwJTsqL1xufVxuXG4jcmVwb3J0IHtcbiAgei1pbmRleDogMTAwMTtcbiAgcG9zaXRpb246IGFic29sdXRlO1xuICBib3R0b206IDA7XG4gIGZvbnQ6IDAuOGVtIHNhbnMtc2VyaWY7XG4gIGNvbG9yOiB3aGVhdDtcbiAgdGV4dC1hbGlnbjogY2VudGVyO1xuICB3aWR0aDogNjAlO1xuICBsZWZ0OiAyMCU7XG59Il19 */"

/***/ }),

/***/ "./src/app/map/time-series/time-series.component.ts":
/*!**********************************************************!*\
  !*** ./src/app/map/time-series/time-series.component.ts ***!
  \**********************************************************/
/*! exports provided: TimeSeriesComponent */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TimeSeriesComponent", function() { return TimeSeriesComponent; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js");
/* harmony import */ var jquery__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(jquery__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../services/map-service/map.service */ "./src/app/services/map-service/map.service.ts");
/* harmony import */ var _services_time_time_service__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../services/time/time.service */ "./src/app/services/time/time.service.ts");
/* harmony import */ var highcharts_highstock__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! highcharts/highstock */ "./node_modules/highcharts/highstock.js");
/* harmony import */ var highcharts_highstock__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(highcharts_highstock__WEBPACK_IMPORTED_MODULE_5__);
/**
 * @Summary: Time chart that can be used to select time range.
 *
 * @Author: (Hugo) Qiaonan Huang, Yang Cao
 *
 * Last modified  : 2019-08-27 15:31:40
 */






let TimeSeriesComponent = class TimeSeriesComponent {
    constructor(mapService, timeService) {
        this.mapService = mapService;
        this.timeService = timeService;
        this.timeRangeChange = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
        this.halfUnit = 86400000 / 2;
        this.currentTick = undefined;
        this.hasPlotBand = false;
        /**
         * Using tweet data to draw a time series reflecting daily tweet information
         *
         * Get data from backend and do the data retrieval of time to a specific date.
         * Count wildfire related tweets and draw it as a time series chart to visualize.
         *
         * @param tweets tweet data crawled using tweet api
         *
         */
        this.drawTimeSeries = (tweets) => {
            /**
             *  Refine tweet data to count related to 'wildfire' in each DAY,
             *  storing in charData.
             */
            const chartData = [];
            const dailyCount = {};
            for (const tweet of tweets) {
                const createAt = tweet.create_at.split('T')[0];
                if (dailyCount.hasOwnProperty(createAt)) {
                    dailyCount[createAt]++;
                }
                else {
                    dailyCount[createAt] = 1;
                }
            }
            Object.keys(dailyCount).sort().forEach(key => {
                chartData.push([new Date(key).getTime(), dailyCount[key]]);
            });
            /** Plotting format of time-series. */
            const timeseries = highcharts_highstock__WEBPACK_IMPORTED_MODULE_5__["stockChart"]('timebar-container', {
                chart: {
                    height: 150,
                    backgroundColor: undefined,
                    zoomType: 'x',
                    events: {
                        /**
                         *  Tow things to check on a click event:
                         *  1. Plot band: transparent orange box drew on time-series.
                         *  2. Ticks (x-axis label): color the x-axis if it is labeled.
                         */
                        click: event => {
                            // @ts-ignore
                            const [leftBandStart, bandCenter, rightBandEnd, tick] = this.closestTickNearClick(event.xAxis[0]);
                            const dateSelectedInYMD = new Date(bandCenter).toISOString().substring(0, 10);
                            if (!this.hasPlotBand) {
                                timeseries.xAxis[0].addPlotBand({
                                    from: leftBandStart,
                                    to: rightBandEnd,
                                    color: 'rgba(216,128,64,0.25)',
                                    id: 'plotBand',
                                });
                                if (tick !== undefined) {
                                    tick.label.css({
                                        color: '#ffffff'
                                    });
                                }
                                this.currentTick = tick;
                                this.hasPlotBand = true;
                                this.timeService.setCurrentDate(dateSelectedInYMD);
                            }
                            else if (dateSelectedInYMD !== this.timeService.getCurrentDate()) {
                                timeseries.xAxis[0].removePlotBand('plotBand');
                                timeseries.xAxis[0].addPlotBand({
                                    from: leftBandStart,
                                    to: rightBandEnd,
                                    color: 'rgba(216,128,64,0.25)',
                                    id: 'plotBand'
                                });
                                if (this.currentTick !== undefined && this.currentTick.hasOwnProperty('label')) {
                                    this.currentTick.label.css({
                                        color: '#666666'
                                    });
                                }
                                if (tick !== undefined) {
                                    tick.label.css({
                                        color: '#ffffff'
                                    });
                                }
                                this.currentTick = tick;
                                this.timeService.setCurrentDate(dateSelectedInYMD);
                            }
                            else {
                                timeseries.xAxis[0].removePlotBand('plotBand');
                                if (this.currentTick !== undefined && this.currentTick.hasOwnProperty('label')) {
                                    this.currentTick.label.css({
                                        color: '#666666'
                                    });
                                }
                                this.currentTick = undefined;
                                this.hasPlotBand = false;
                                this.timeService.setCurrentDate(undefined);
                            }
                        },
                    }
                },
                navigator: {
                    margin: 2,
                    height: 30,
                },
                title: {
                    text: '',
                },
                series: [{
                        type: 'line',
                        data: chartData,
                        color: '#e25822',
                        name: '<span style=\'color:#e25822\'>Wildfire Tweet</span>',
                    }],
                tooltip: {
                    enabled: true,
                    backgroundColor: 'rgba(255,255,255,0)',
                    padding: 0,
                    hideDelay: 0,
                    style: {
                        color: '#ffffff',
                    }
                },
                rangeSelector: {
                    enabled: false
                },
                xAxis: {
                    type: 'datetime',
                    range: 6 * 30 * 24 * 3600 * 1000,
                    events: {
                        /**
                         *  This event allow both selections on time-series and navigator,
                         *  updating information of date.
                         */
                        setExtremes: (event) => {
                            this.timeService.setRangeDate(event.min + this.halfUnit, event.max);
                            jquery__WEBPACK_IMPORTED_MODULE_2__('#report').html('Date Range => ' +
                                'Start: ' + highcharts_highstock__WEBPACK_IMPORTED_MODULE_5__["dateFormat"]('%Y-%m-%d', event.min) +
                                ', End: ' + highcharts_highstock__WEBPACK_IMPORTED_MODULE_5__["dateFormat"]('%Y-%m-%d', event.max));
                            jquery__WEBPACK_IMPORTED_MODULE_2__(window).trigger('timeRangeChange');
                        }
                    }
                },
                scrollbar: {
                    height: 0,
                },
            });
        };
    }
    ngOnInit() {
        /** Subscribe tweet data related to wildfire in service. */
        this.mapService.getFireTweetData().subscribe(data => this.drawTimeSeries(data));
    }
    /**
     *  Summary: Generate information needed for click event.
     *
     *  Description: Receive a event axis with click value to measure the distance on time series.
     *
     *  @param eventAxis Click event fire information of axis.
     *
     *  @return [leftBandStart, bandCenter, rightBandEnd, tick] which will be used in
     *  time series click event.
     */
    closestTickNearClick(eventAxis) {
        const halfUnitDistance = 43200000;
        const xAxis = eventAxis.axis;
        const dateClickedInMs = eventAxis.value;
        let distanceToTheLeft;
        let distanceToTheRight;
        let minValue;
        let minKey;
        if (xAxis.ordinalPositions === undefined) {
            /** Ticks evenly distributed with unit distance 43200000*2. */
            minValue = dateClickedInMs - dateClickedInMs % halfUnitDistance;
            minValue += minValue % (halfUnitDistance * 2);
            distanceToTheLeft = halfUnitDistance;
            distanceToTheRight = halfUnitDistance;
        }
        else {
            /** Ticks distributed with different distance. */
            xAxis.ordinalPositions.forEach((value, index) => {
                if (minValue === undefined || Math.abs(dateClickedInMs - value) < Math.abs(dateClickedInMs - minValue)) {
                    minValue = value;
                    minKey = index;
                }
            });
            if (minKey === 0 || minKey === xAxis.ordinalPositions.length - 1) {
                /** Case when click at the beginning or the end of the range. */
                distanceToTheLeft = 0;
                distanceToTheRight = 0;
            }
            else {
                distanceToTheLeft = (xAxis.ordinalPositions[minKey] - xAxis.ordinalPositions[minKey - 1]) / 2;
                distanceToTheRight = (xAxis.ordinalPositions[minKey + 1] - xAxis.ordinalPositions[minKey]) / 2;
            }
        }
        return [minValue - distanceToTheLeft, minValue, distanceToTheRight + minValue, xAxis.ticks[minValue]];
    }
};
TimeSeriesComponent.ctorParameters = () => [
    { type: _services_map_service_map_service__WEBPACK_IMPORTED_MODULE_3__["MapService"] },
    { type: _services_time_time_service__WEBPACK_IMPORTED_MODULE_4__["TimeService"] }
];
tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Output"])()
], TimeSeriesComponent.prototype, "timeRangeChange", void 0);
TimeSeriesComponent = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Component"])({
        selector: 'app-time-series',
        template: __webpack_require__(/*! raw-loader!./time-series.component.html */ "./node_modules/raw-loader/index.js!./src/app/map/time-series/time-series.component.html"),
        styles: [__webpack_require__(/*! ./time-series.component.css */ "./src/app/map/time-series/time-series.component.css")]
    })
], TimeSeriesComponent);



/***/ }),

/***/ "./src/app/services/fire-service/fire.service.ts":
/*!*******************************************************!*\
  !*** ./src/app/services/fire-service/fire.service.ts ***!
  \*******************************************************/
/*! exports provided: FireService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "FireService", function() { return FireService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../environments/environment */ "./src/environments/environment.ts");





let FireService = class FireService {
    constructor(http) {
        this.http = http;
    }
    searchFirePolygon(id, size) {
        return this.http.post(`http://${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].host}:${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].port}/data/fire-with-id`, JSON.stringify({
            id,
            size
        }));
    }
    searchSeparatedFirePolygon(id, size) {
        return this.http.post(`http://${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].host}:${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].port}/data/fire-with-id-seperated`, JSON.stringify({
            id, size,
        })).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(data => {
            return { type: 'FeatureCollection', features: data };
        }));
    }
};
FireService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"] }
];
FireService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], FireService);



/***/ }),

/***/ "./src/app/services/map-service/map.service.ts":
/*!*****************************************************!*\
  !*** ./src/app/services/map-service/map.service.ts ***!
  \*****************************************************/
/*! exports provided: MapService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "MapService", function() { return MapService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");
/* harmony import */ var rxjs_operators__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! rxjs/operators */ "./node_modules/rxjs/_esm2015/operators/index.js");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ../../../environments/environment */ "./src/environments/environment.ts");





let MapService = class MapService {
    constructor(http) {
        this.http = http;
        // Declare data events for components to action
        this.temperatureChangeEvent = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
        this.searchMarkerLoaded = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
        this.hoverMarkerLoaded = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
        this.markerRemove = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
        this.searchNameLoaded = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
        this.sendFireToFront = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
    }
    getFireTweetData() {
        return this.http.get(`http://${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].host}:${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].port}/tweet/fire-tweet`);
    }
    getWildfirePredictionData(northEastBoundaries, southWestBoundaries, start, end) {
        return this.http.post(`http://${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].host}:${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].port}/wildfire-prediction`, JSON.stringify({
            northEast: northEastBoundaries,
            southWest: southWestBoundaries,
            startDate: start,
            endDate: end,
        }));
    }
    getFirePolygonData(northEastBoundaries, southWestBoundaries, setSize, start, end) {
        return this.http.post(`http://${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].host}:${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].port}/data/fire-polygon`, JSON.stringify({
            northEast: northEastBoundaries,
            southWest: southWestBoundaries,
            size: setSize,
            startDate: start,
            endDate: end,
        })).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(data => {
            return { type: 'FeatureCollection', features: data };
        }));
    }
    getWindData() {
        return this.http.get(`http://${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].host}:${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].port}/data/wind`);
    }
    getBoundaryData(stateLevel, countyLevel, cityLevel, northEastBoundaries, southWestBoundaries) {
        return this.http.post(`http://${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].host}:${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].port}/search/boundaries`, JSON.stringify({
            states: stateLevel,
            cities: cityLevel,
            counties: countyLevel,
            northEast: northEastBoundaries,
            southWest: southWestBoundaries,
        })).pipe(Object(rxjs_operators__WEBPACK_IMPORTED_MODULE_3__["map"])(data => {
            return { type: 'FeatureCollection', features: data };
        }));
    }
    getDropBox(userInput) {
        // gets auto-completion suggestions
        return this.http.get(`http://${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].host}:${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].port}/dropdownMenu`, { params: new _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpParams"]().set('userInput', userInput) });
    }
    getRecentTweetData() {
        return this.http.get(`http://${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].host}:${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].port}/tweet/recent-tweet`);
    }
    getTemperatureData() {
        return this.http.get(`http://${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].host}:${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].port}/data/recent-temp`);
    }
    getClickData(lat, lng, radius, timestamp, range) {
        return this.http.post(`http://${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].host}:${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].port}/data/aggregation`, JSON.stringify({
            lat, lng, radius, timestamp, range
        }));
    }
    getIntentTweetData(id) {
        return this.http.get(`http://${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].host}:${_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].port}/tweet/tweet-from-id`, { params: new _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpParams"]().set('tweet_id', id) });
    }
};
MapService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"] }
];
MapService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], MapService);



/***/ }),

/***/ "./src/app/services/search/search.service.ts":
/*!***************************************************!*\
  !*** ./src/app/services/search/search.service.ts ***!
  \***************************************************/
/*! exports provided: SearchService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "SearchService", function() { return SearchService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_common_http__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/common/http */ "./node_modules/@angular/common/fesm2015/http.js");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ../../../environments/environment */ "./src/environments/environment.ts");




let SearchService = class SearchService {
    constructor(http) {
        this.http = http;
        this.searchDataLoaded = new _angular_core__WEBPACK_IMPORTED_MODULE_1__["EventEmitter"]();
    }
    getSearch(userInput) {
        return this.http.get(`http://${_environments_environment__WEBPACK_IMPORTED_MODULE_3__["environment"].host}:${_environments_environment__WEBPACK_IMPORTED_MODULE_3__["environment"].port}/search`, { params: new _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpParams"]().set('keyword', userInput) });
    }
};
SearchService.ctorParameters = () => [
    { type: _angular_common_http__WEBPACK_IMPORTED_MODULE_2__["HttpClient"] }
];
SearchService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
], SearchService);



/***/ }),

/***/ "./src/app/services/time/time.service.ts":
/*!***********************************************!*\
  !*** ./src/app/services/time/time.service.ts ***!
  \***********************************************/
/*! exports provided: TimeService */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "TimeService", function() { return TimeService; });
/* harmony import */ var tslib__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! tslib */ "./node_modules/tslib/tslib.es6.js");
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/**
 * @Summary: TimeService as one separate service that allows other components to get time.
 *
 * @Description: Initial current time range from previous 6 months to present.
 *
 * @Author: (Hugo) Qiaonan Huang
 *
 * Last modified  : 2019-08-27 15:31:40
 */


// import {Observable, Subject, BehaviorSubject} from 'rxjs';
// import {HttpClient, HttpParams} from '@angular/common/http';
let TimeService = 
/**
 * @param currentDateInYMD    Current date in yyyy-mm-dd, used in click event in time series.
 * @param rangeStartDateInMS  Range start time in millisecond, used in selection event in time series.
 * @param rangeEndDateInMS    Range end time in millisecond, used in selection event in time series.
 *
 */
class TimeService {
    constructor() {
        this.currentDateInYMD = undefined;
        this.rangeStartDateInMS = new Date().getTime() - 6 * 30 * 24 * 3600 * 1000;
        this.rangeEndDateInMS = new Date().getTime();
    }
    setCurrentDate(dateInYMD) {
        this.currentDateInYMD = dateInYMD;
    }
    setRangeDate(startInMs, endInMs) {
        this.rangeStartDateInMS = startInMs;
        this.rangeEndDateInMS = endInMs;
    }
    getCurrentDate() {
        return this.currentDateInYMD !== undefined ? this.currentDateInYMD : new Date().toISOString().substring(0, 10);
    }
    getRangeDate() {
        return [this.rangeStartDateInMS, this.rangeEndDateInMS];
    }
};
TimeService = tslib__WEBPACK_IMPORTED_MODULE_0__["__decorate"]([
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["Injectable"])({
        providedIn: 'root'
    })
    /**
     * @param currentDateInYMD    Current date in yyyy-mm-dd, used in click event in time series.
     * @param rangeStartDateInMS  Range start time in millisecond, used in selection event in time series.
     * @param rangeEndDateInMS    Range end time in millisecond, used in selection event in time series.
     *
     */
], TimeService);



/***/ }),

/***/ "./src/environments/environment.ts":
/*!*****************************************!*\
  !*** ./src/environments/environment.ts ***!
  \*****************************************/
/*! exports provided: environment */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "environment", function() { return environment; });
// This file can be replaced during build by using the `fileReplacements` array.
// `ng build --prod` replaces `environment.ts` with `environment.prod.ts`.
// The list of file replacements can be found in `angular.json`.
const environment = {
    production: false,
    host: '127.0.0.1',
    port: 5000
};
/*
 * For easier debugging in development mode, you can import the following file
 * to ignore zone related error stack frames such as `zone.run`, `zoneDelegate.invokeTask`.
 *
 * This import should be commented out in production mode because it will have a negative impact
 * on performance if an error is thrown.
 */
// import 'zone.js/dist/zone-error';  // Included with Angular CLI.


/***/ }),

/***/ "./src/main.ts":
/*!*********************!*\
  !*** ./src/main.ts ***!
  \*********************/
/*! no exports provided */
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony import */ var hammerjs__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! hammerjs */ "./node_modules/hammerjs/hammer.js");
/* harmony import */ var hammerjs__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(hammerjs__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _angular_core__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @angular/core */ "./node_modules/@angular/core/fesm2015/core.js");
/* harmony import */ var _angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @angular/platform-browser-dynamic */ "./node_modules/@angular/platform-browser-dynamic/fesm2015/platform-browser-dynamic.js");
/* harmony import */ var _app_app_module__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./app/app.module */ "./src/app/app.module.ts");
/* harmony import */ var _environments_environment__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./environments/environment */ "./src/environments/environment.ts");





if (_environments_environment__WEBPACK_IMPORTED_MODULE_4__["environment"].production) {
    Object(_angular_core__WEBPACK_IMPORTED_MODULE_1__["enableProdMode"])();
}
Object(_angular_platform_browser_dynamic__WEBPACK_IMPORTED_MODULE_2__["platformBrowserDynamic"])().bootstrapModule(_app_app_module__WEBPACK_IMPORTED_MODULE_3__["AppModule"])
    .catch(err => console.error(err));


/***/ }),

/***/ 0:
/*!***************************!*\
  !*** multi ./src/main.ts ***!
  \***************************/
/*! no static exports found */
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__(/*! /Users/yang/Desktop/cs199/wildfireDev/frontend/src/main.ts */"./src/main.ts");


/***/ })

},[[0,"runtime","vendor"]]]);
//# sourceMappingURL=main.js.map