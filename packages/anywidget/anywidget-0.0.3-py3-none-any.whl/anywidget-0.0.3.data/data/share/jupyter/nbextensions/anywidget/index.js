// package.json
var name = "anywidget";
var version = "0.0.3";

// src/widget.js
function widget_default(base) {
  class AnyModel extends base.DOMWidgetModel {
    static model_name = "AnyModel";
    static model_module = name;
    static model_module_version = version;
    static view_name = "AnyView";
    static view_module = name;
    static view_module_version = version;
  }
  class AnyView extends base.DOMWidgetView {
    async render() {
      let widget;
      let esm = this.model.get("_module");
      if (esm.startsWith("http://") || esm.startsWith("https://")) {
        widget = await import(
          /* webpackIgnore: true */
          esm
        );
      } else {
        let url = URL.createObjectURL(
          new Blob([esm], { type: "text/javascript" })
        );
        widget = await import(
          /* webpackIgnore: true */
          url
        );
        URL.revokeObjectURL(url);
      }
      await widget.render(this);
    }
  }
  return { AnyModel, AnyView };
}

// src/index.js
define(["@jupyter-widgets/base"], widget_default);
