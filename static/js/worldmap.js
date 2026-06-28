/**
 * Volumus Global — Animated D3 World Map
 * Highlights service countries with pulsing glow effect
 */
(function () {
  'use strict';

  const HIGHLIGHTED = {
    356: { name: 'India',        flag: '🇮🇳', services: ['Tax & Compliance', 'Bookkeeping', 'Digital Consulting'] },
    840: { name: 'United States',flag: '🇺🇸', services: ['M&A Advisory', 'Digital Transformation', 'Finance Consulting'] },
    124: { name: 'Canada',       flag: '🇨🇦', services: ['Cross-Border M&A', 'Tax Planning', 'Business Structuring'] },
    554: { name: 'New Zealand',  flag: '🇳🇿', services: ['Business Structuring', 'Tax Advisory', 'Regulatory Compliance'] },
    710: { name: 'South Africa', flag: '🇿🇦', services: ['Investment Advisory', 'B-BBEE Compliance', 'Corporate Governance'] },
    36:  { name: 'Australia',    flag: '🇦🇺', services: ['Corporate Governance', 'Tax Compliance', 'ASIC Advisory'] },
  };

  const COLOR_DEFAULT    = '#1E3A5F';
  const COLOR_HIGHLIGHT  = '#2D7DD2';
  const COLOR_HOVER      = '#5AA3EE';
  const COLOR_OCEAN      = '#071628';
  const COLOR_BORDER     = '#0C2340';

  function initMap() {
    const container = document.getElementById('world-map-container');
    if (!container) return;

    const W = container.clientWidth || 900;
    const H = Math.round(W * 0.52);

    const svg = d3.select('#world-map-svg')
      .attr('viewBox', `0 0 ${W} ${H}`)
      .attr('preserveAspectRatio', 'xMidYMid meet');

    // Ocean background
    svg.append('rect')
      .attr('width', W).attr('height', H)
      .attr('fill', COLOR_OCEAN)
      .attr('rx', 12);

    const projection = d3.geoNaturalEarth1()
      .scale(W / 6.5)
      .translate([W / 2, H / 2]);

    const path = d3.geoPath().projection(projection);

    // Defs for glow filter
    const defs = svg.append('defs');

    // Glow filter for highlighted countries
    const glowFilter = defs.append('filter')
      .attr('id', 'glow')
      .attr('x', '-30%').attr('y', '-30%')
      .attr('width', '160%').attr('height', '160%');
    glowFilter.append('feGaussianBlur')
      .attr('stdDeviation', '3').attr('result', 'coloredBlur');
    const feMerge = glowFilter.append('feMerge');
    feMerge.append('feMergeNode').attr('in', 'coloredBlur');
    feMerge.append('feMergeNode').attr('in', 'SourceGraphic');

    // Pulse ring filter
    const pulseFilter = defs.append('filter')
      .attr('id', 'pulse')
      .attr('x', '-50%').attr('y', '-50%')
      .attr('width', '200%').attr('height', '200%');
    pulseFilter.append('feGaussianBlur')
      .attr('stdDeviation', '6').attr('result', 'coloredBlur');
    const feMerge2 = pulseFilter.append('feMerge');
    feMerge2.append('feMergeNode').attr('in', 'coloredBlur');
    feMerge2.append('feMergeNode').attr('in', 'SourceGraphic');

    // Graticule
    const graticule = d3.geoGraticule();
    svg.append('path')
      .datum(graticule())
      .attr('d', path)
      .attr('fill', 'none')
      .attr('stroke', 'rgba(45,125,210,0.08)')
      .attr('stroke-width', 0.5);

    // Tooltip
    const tooltip = d3.select('#map-tooltip');

    // Load world topojson
    const topoUrl = 'https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json';

    d3.json(topoUrl).then(function (world) {
      const countries = topojson.feature(world, world.objects.countries);

      // Draw all countries
      const countryPaths = svg.selectAll('.country')
        .data(countries.features)
        .enter()
        .append('path')
        .attr('class', 'country')
        .attr('d', path)
        .attr('fill', d => HIGHLIGHTED[+d.id] ? COLOR_HIGHLIGHT : COLOR_DEFAULT)
        .attr('stroke', COLOR_BORDER)
        .attr('stroke-width', 0.4)
        .attr('filter', d => HIGHLIGHTED[+d.id] ? 'url(#glow)' : null)
        .style('cursor', d => HIGHLIGHTED[+d.id] ? 'pointer' : 'default');

      // Hover interaction
      countryPaths
        .on('mouseenter', function (event, d) {
          const info = HIGHLIGHTED[+d.id];
          if (!info) return;

          d3.select(this)
            .attr('fill', COLOR_HOVER)
            .attr('stroke-width', 1.2);

          const [x, y] = d3.pointer(event, container);
          tooltip
            .style('left', (x + 16) + 'px')
            .style('top',  (y - 20) + 'px')
            .classed('visible', true)
            .html(`<strong>${info.flag} ${info.name}</strong><br>${info.services.map(s => `• ${s}`).join('<br>')}`);
        })
        .on('mouseleave', function (event, d) {
          const info = HIGHLIGHTED[+d.id];
          if (!info) return;

          d3.select(this)
            .attr('fill', COLOR_HIGHLIGHT)
            .attr('stroke-width', 0.4);

          tooltip.classed('visible', false);
        })
        .on('click', function (event, d) {
          const info = HIGHLIGHTED[+d.id];
          if (!info) return;
          window.location.href = '/countries';
        });

      // Draw pulsing rings on country centroids
      const highlightedFeatures = countries.features.filter(d => HIGHLIGHTED[+d.id]);

      highlightedFeatures.forEach(function (d) {
        const centroid = path.centroid(d);
        if (!centroid || isNaN(centroid[0])) return;
        const info = HIGHLIGHTED[+d.id];

        // Outer pulse ring
        const ring = svg.append('circle')
          .attr('cx', centroid[0])
          .attr('cy', centroid[1])
          .attr('r', 8)
          .attr('fill', 'none')
          .attr('stroke', COLOR_HOVER)
          .attr('stroke-width', 1.5)
          .attr('opacity', 0.8);

        function animateRing() {
          ring
            .attr('r', 8)
            .attr('opacity', 0.8)
            .transition()
            .duration(2000)
            .ease(d3.easeCubicOut)
            .attr('r', 28)
            .attr('opacity', 0)
            .on('end', animateRing);
        }

        // Stagger animations
        const delay = Object.keys(HIGHLIGHTED).indexOf(String(d.id)) * 350;
        setTimeout(animateRing, delay);

        // Inner dot
        svg.append('circle')
          .attr('cx', centroid[0])
          .attr('cy', centroid[1])
          .attr('r', 4)
          .attr('fill', '#5AA3EE')
          .attr('filter', 'url(#glow)')
          .attr('opacity', 0.9);

        // Country label
        svg.append('text')
          .attr('x', centroid[0])
          .attr('y', centroid[1] - 12)
          .attr('text-anchor', 'middle')
          .attr('font-size', '8px')
          .attr('font-family', 'Inter, sans-serif')
          .attr('font-weight', '600')
          .attr('fill', 'rgba(255,255,255,0.85)')
          .attr('letter-spacing', '0.05em')
          .text(info.name.toUpperCase());
      });

      // Borders between countries
      svg.append('path')
        .datum(topojson.mesh(world, world.objects.countries, (a, b) => a !== b))
        .attr('d', path)
        .attr('fill', 'none')
        .attr('stroke', COLOR_BORDER)
        .attr('stroke-width', 0.3);

    }).catch(function (err) {
      console.warn('Map data could not be loaded:', err);
      container.innerHTML = '<p style="color:rgba(255,255,255,0.4);text-align:center;padding:2rem;">Map loading...</p>';
    });
  }

  // Init after DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMap);
  } else {
    initMap();
  }

  // Re-init on resize (debounced)
  let resizeTimer;
  window.addEventListener('resize', function () {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function () {
      const svg = document.getElementById('world-map-svg');
      if (svg) { svg.innerHTML = ''; initMap(); }
    }, 250);
  });
})();
