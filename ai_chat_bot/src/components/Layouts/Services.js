import React from 'react';
import { useInView } from 'react-intersection-observer';
import './Services.css';

function Services() {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.5,
  });

  return (
    <section
      id="services"
      ref={ref}
      className={`section ${inView ? 'fade-in' : ''}`}
    >
      <h2>Our Services</h2>
      <p>Explore the services we provide to make your life easier.</p>
    </section>
  );
}

export default Services;
