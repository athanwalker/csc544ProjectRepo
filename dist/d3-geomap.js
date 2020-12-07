// https://d3-geomap.github.io v3.3.0 Copyright 2020 Ramiro Gómez
(function (global, factory) {
typeof exports === 'object' && typeof module !== 'undefined' ? factory(exports, require('d3-selection'), require('d3-transition'), require('topojson'), require('d3-fetch'), require('d3-geo'), require('d3-array'), require('d3-scale'), require('d3-format')) :
typeof define === 'function' && define.amd ? define(['exports', 'd3-selection', 'd3-transition', 'topojson', 'd3-fetch', 'd3-geo', 'd3-array', 'd3-scale', 'd3-format'], factory) :
(global = global || self, factory(global.d3 = global.d3 || {}, global.d3, global.d3, global.topojson, global.d3, global.d3, global.d3, global.d3, global.d3));
}(this, (function (exports, d3Selection, d3Transition, topojson, d3Fetch, d3Geo, d3Array, d3Scale, d3Format) { 'use strict';

function addAccessor(obj, name, value) {
  obj[name] = _ => {
    if (typeof _ === 'undefined') return obj.properties[name] || value;
    obj.properties[name] = _;
    return obj;
  };
}

class Geomap {
  constructor() {
    // Set default properties optimized for naturalEarth projection.
    this.properties = {
      /**
       * URL to TopoJSON file to load when geomap is drawn. Ignored if geoData is specified.
       *
       * @type {string|null}
       */
      geofile: null,

      /**
       * Contents of TopoJSON file. If specified, geofile is ignored.
       *
       * @type {Promise<object>|object|null}
       */
      geoData: null,
      height: null,
      postUpdate: null,
      projection: d3Geo.geoNaturalEarth1,
      rotate: [0, 0, 0],
      scale: null,
      translate: null,
      unitId: 'iso3',
      unitPrefix: 'unit-',
      units: 'units',
      unitTitle: d => d.properties.name,
      width: null,
      zoomFactor: 4
    }; // Setup methods to access properties.

    for (let key in this.properties) addAccessor(this, key, this.properties[key]); // Store internal properties.


    this._ = {};
  }

  clicked(d) {
    let k = 1,
        x0 = this.properties.width / 2,
        y0 = this.properties.height / 2,
        x = x0,
        y = y0;

    if (d && d.hasOwnProperty('geometry') && this._.centered !== d) {
      let centroid = this.path.centroid(d);
      x = centroid[0];
      y = centroid[1];
      k = this.properties.zoomFactor;
      this._.centered = d;
    } else {
      this._.centered = null;
    }

    this.svg.selectAll('path.unit').classed('active', this._.centered && (_ => _ === this._.centered));
    this.svg.selectAll('g.zoom').transition().duration(750).attr('transform', `translate(${x0}, ${y0})scale(${k})translate(-${x}, -${y})`);
  }
  /**
   * Load geo data once here and draw map. Call update at the end.
   *
   * By default map dimensions are calculated based on the width of the
   * selection container element so they are responsive. Properties set before
   * will be kept.
   */


  draw(selection) {
    let self = this;
    self.data = selection.datum();
    if (!self.properties.width) self.properties.width = selection.node().getBoundingClientRect().width;
    if (!self.properties.height) self.properties.height = self.properties.width / 1.92;
    if (!self.properties.scale) self.properties.scale = self.properties.width / 5.4;
    if (!self.properties.translate) self.properties.translate = [self.properties.width / 2, self.properties.height / 2];
    self.svg = selection.append('svg').attr('width', self.properties.width).attr('height', self.properties.height);
    self.svg.append('rect').attr('class', 'background').attr('width', self.properties.width).attr('height', self.properties.height).on('click', self.clicked.bind(self)); // Set map projection and path.

    let proj = self.properties.projection().scale(self.properties.scale).translate(self.properties.translate).precision(.1); // Not every projection supports rotation, e. g. albersUsa does not.

    if (proj.hasOwnProperty('rotate') && self.properties.rotate) proj.rotate(self.properties.rotate);
    self.path = d3Geo.geoPath().projection(proj);

    const drawGeoData = geo => {
      self.geo = geo;
      self.svg.append('g').attr('class', 'units zoom').selectAll('path').data(topojson.feature(geo, geo.objects[self.properties.units]).features).enter().append('path').attr('class', d => 'unit ' + this.properties.unitPrefix + self.unitName(d.properties)).attr('d', self.path).on('click', self.clicked.bind(self)).append('title').text(self.properties.unitTitle);
      self.update();
    };

    Promise.resolve().then(() => {
      if (self.properties.geoData) {
        return self.properties.geoData;
      }

      return d3Fetch.json(self.properties.geofile);
    }).then(geo => drawGeoData(geo));
  }

  unitName(record) {
    let name = record[this.properties.unitId];

    if ('undefined' !== typeof name) {
      return name.toString().trim().replace(/\s/g, '_');
    }

    return '';
  }

  update() {
    if (this.properties.postUpdate) this.properties.postUpdate();
  }

}

const D3_CHROMATIC_SCHEME_OrBl9 = ['#f7fbff', '#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b'];
class Choropleth extends Geomap {
  constructor() {
    super();
    let properties = {
      colors: Choropleth.DEFAULT_COLORS,
      column: null,
      domain: null,
      duration: null,
      format: d3Format.format(',.02f'),
      legend: false,
      valueScale: d3Scale.scaleQuantize
    };

    for (let key in properties) {
      this.properties[key] = properties[key];
      addAccessor(this, key, properties[key]);
    }
  }

  columnVal(d) {
    return +d[this.properties.column];
  }

  defined(val) {
    return !(isNaN(val) || 'undefined' === typeof val || '' === val);
  }

  update() {
    let self = this;
    self.extent = d3Array.extent(self.data, self.columnVal.bind(self));
    self.colorScale = self.properties.valueScale().domain(self.properties.domain || self.extent).range(D3_CHROMATIC_SCHEME_OrBl9); // Remove fill styles that may have been set previously.

    self.svg.selectAll('path.unit').style('fill', null); // Add new fill styles based on data values.

    self.data.forEach(d => {
      let uid = self.unitName(d),
          val = d[self.properties.column].toString().trim(); // selectAll must be called and not just select, otherwise the data
      // attribute of the selected path object is overwritten with self.data.

      let unit = self.svg.selectAll(`.${self.properties.unitPrefix}${uid}`); // Data can contain values for non existing units and values can be empty or NaN.

      if (!unit.empty() && self.defined(val)) {
        let fill = self.colorScale(val),
            text = self.properties.unitTitle(unit.datum());
        if (self.properties.duration) unit.transition().duration(self.properties.duration).style('fill', fill);else unit.style('fill', fill); // New title with column and value.

        val = self.properties.format(val);
        unit.select('title').text(`${text}\n\n${self.properties.column}: ${val}`);
      }
    });
    if (self.properties.legend) self.drawLegend(self.properties.legend); // Make sure postUpdate function is run if set.

    super.update();
  } ////////////////////////////////////////////////////////

  /**
   * Draw legend including color scale and labels.
   *
   * If bounds is set to true, legend dimensions will be calculated based on
   * the map dimensions. Otherwise bounds must be an object with width and
   * height attributes.
   */


  drawLegend(bounds = null) {
    let self = this,
        steps = D3_CHROMATIC_SCHEME_OrBl9.length,
        wBox,
        hBox;
    const wFactor = 10,
          hFactor = 3;

    if (bounds === true) {
      wBox = self.properties.width / wFactor;
      hBox = self.properties.height / hFactor;
    } else {
      wBox = bounds.width;
      hBox = bounds.height;
    }

    const wRect = wBox / (wFactor * .75),
          hLegend = hBox - hBox / (hFactor * 1.8),
          offsetText = wRect / 2,
          offsetY = self.properties.height - hBox,
          tr = 'translate(' + offsetText + ',' + offsetText * 3 + ')'; // Remove possibly existing legend, before drawing.

    self.svg.select('g.legend').remove(); // Reverse a copy to not alter colors array.

    const colors = D3_CHROMATIC_SCHEME_OrBl9.slice().reverse(),
          hRect = hLegend / steps,
          offsetYFactor = hFactor / hRect;
    let legend = self.svg.append('g').attr('class', 'legend').attr('width', wBox).attr('height', hBox).attr('transform', 'translate(0,' + offsetY + ')');
    legend.append('rect').style('fill', '#fff').attr('class', 'legend-bg').attr('width', wBox).attr('height', hBox); // Draw a rectangle around the color scale to add a border.

    legend.append('rect').attr('class', 'legend-bar').attr('width', wRect).attr('height', hLegend).attr('transform', tr);
    let sg = legend.append('g').attr('transform', tr); // Draw color scale.

    sg.selectAll('rect').data(colors).enter().append('rect').attr('y', (d, i) => i * hRect).attr('fill', (d, i) => colors[i]).attr('width', wRect).attr('height', hRect); // Determine display values for lower and upper thresholds. If the
    // minimum data value is lower than the first element in the domain
    // draw a less than sign. If the maximum data value is larger than the
    // second domain element, draw a greater than sign.

    let minDisplay = self.extent[0],
        maxDisplay = self.extent[1],
        addLower = false,
        addGreater = false;

    if (self.properties.domain) {
      if (self.properties.domain[1] < maxDisplay) addGreater = true;
      maxDisplay = self.properties.domain[1];
      if (self.properties.domain[0] > minDisplay) addLower = true;
      minDisplay = self.properties.domain[0];
    } // Draw color scale labels.


    sg.selectAll('text').data(colors).enter().append('text').text((d, i) => {
      // The last element in the colors list corresponds to the lower threshold.
      if (i === steps - 1) {
        let text = self.properties.format(minDisplay);
        if (addLower) text = `< ${text}`;
        return text;
      }

      return self.properties.format(self.colorScale.invertExtent(d)[0]);
    }).attr('class', (d, i) => 'text-' + i).attr('x', wRect + offsetText).attr('y', (d, i) => i * hRect + (hRect + hRect * offsetYFactor)); // Draw label for end of extent.

    sg.append('text').text(() => {
      let text = self.properties.format(maxDisplay);
      if (addGreater) text = `> ${text}`;
      return text;
    }).attr('x', wRect + offsetText).attr('y', offsetText * offsetYFactor * 2);
  }

}
Choropleth.DEFAULT_COLORS = D3_CHROMATIC_SCHEME_OrBl9;

function geomap() {
  return new Geomap();
}

function choropleth() {
  return new Choropleth();
}

exports.choropleth = choropleth;
exports.geomap = geomap;

Object.defineProperty(exports, '__esModule', { value: true });

})));
