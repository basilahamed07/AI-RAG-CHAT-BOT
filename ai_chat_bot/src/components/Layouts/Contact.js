import React from 'react';
import { useInView } from 'react-intersection-observer';
import './Contact.css';

function Contact() {
  const { ref, inView } = useInView({
    triggerOnce: true,
    threshold: 0.5,
  });

  return (
    <section
      id="contact"
      ref={ref}
      className={`section ${inView ? 'fade-in' : ''}`}
    >
      <h2>Contact Us</h2>
      <p>Get in touch with us for any inquiries.</p>
    </section>
  );
}

export default Contact;
