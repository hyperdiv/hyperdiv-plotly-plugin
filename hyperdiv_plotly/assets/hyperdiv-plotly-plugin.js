(() => {
  const hyperdiv = window.hyperdiv;

  hyperdiv.registerPlugin("plotly_chart", (key, domElement, props) => {
    const Plotly = window.Plotly;

    const elem = document.createElement("div");
    elem.style.position = "relative";
    elem.style.height = "100%";
    elem.style.width = "100%";
    domElement.appendChild(elem);

    const chartConfig = {
      data: props.fig.data,
      layout: props.fig.layout,
      browserConfig: props.browser_config,
    };

    Plotly.newPlot(
      elem,
      chartConfig.data,
      chartConfig.layout,
      chartConfig.browserConfig
    ).then(() => {
      window.dispatchEvent(new Event("resize"));
    });

    const resizeObserver = new ResizeObserver(() => {
      window.dispatchEvent(new Event("resize"));
    });

    resizeObserver.observe(elem);

    return (propName, propValue) => {
      if (propName === "fig") {
        chartConfig.data = propValue.data;
        chartConfig.layout = propValue.layout;
      } else if (propName === "browser_config") {
        chartConfig.browserConfig = propValue;
      }

      Plotly.newPlot(
        elem,
        chartConfig.data,
        chartConfig.layout,
        chartConfig.browserConfig
      );
    };
  });
})();
