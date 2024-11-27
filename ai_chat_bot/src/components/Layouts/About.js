import React from 'react';
import { Container, Typography, Box } from '@mui/material';

function About() {
  return (
    <Box sx={{ height: '100vh', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
      <Container maxWidth="md" sx={{ textAlign: 'center' }}>
        <Typography variant="h3" sx={{ mb: 2 }}>About Us</Typography>
        <Typography variant="h6" sx={{ mb: 4 }}>
          We are Chat-Bot, a cutting-edge AI-powered assistant developed by Basil Ahamed. Our goal is to make your life easier by offering instant, smart, and helpful interactions.
        </Typography>
      </Container>
    </Box>
  );
}

export default About;
