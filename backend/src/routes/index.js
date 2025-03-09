const express = require('express');
const router = express.Router();

// Import route modules
const countyRoutes = require('./counties');
const weatherRoutes = require('./weather');
const burnAssessmentRoutes = require('./burn-assessment');
const mapDataRoutes = require('./map-data');

// Use route modules
router.use('/counties', countyRoutes);
router.use('/weather', weatherRoutes);
router.use('/burn-assessment', burnAssessmentRoutes);
router.use('/map', mapDataRoutes);

// API info route
router.get('/', (req, res) => {
  res.json({
    name: 'BurnAI API',
    version: '1.0.0',
    endpoints: [
      '/counties',
      '/weather',
      '/burn-assessment',
      '/map'
    ]
  });
});

module.exports = router; 