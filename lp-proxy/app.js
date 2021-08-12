const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
 
const app = express();
 
app.use('/lp-api', createProxyMiddleware({
  changeOrigin: true,
  target:'https://api.launchpad.net/',
  pathRewrite: {
    '^/lp-api/': '/', // rewrite path
  },
  onProxyRes(proxyRes, req, res) {
    // We want the results from the Launchpad API to get
    // cached by our CDN for a short duration (1 hour).
    proxyRes.headers['cache-control'] = 'public, max-age=3600';
  }
}));
app.listen(8000);
