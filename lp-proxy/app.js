const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
 
const app = express();
 
app.use('/lp-api', createProxyMiddleware({
  changeOrigin: true,
  target:'https://api.launchpad.net/',
  pathRewrite: {
    '^/lp-api/': '/', // rewrite path
  },
}));
app.listen(8000);
