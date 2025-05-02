import React from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const HeroSection = styled.section`
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: ${props => props.theme.colors.gradient};
  position: relative;
  overflow: hidden;
  padding: 4rem 2rem;
  text-align: center;
  clip-path: polygon(0 0, 100% 0, 100% 85%, 0 100%);
  
  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: radial-gradient(circle at center, rgba(0, 168, 255, 0.1) 0%, transparent 70%);
    pointer-events: none;
  }
`;

const HeroTitle = styled(motion.h1)`
  font-size: 4rem;
  color: ${props => props.theme.colors.text};
  margin-bottom: 1.5rem;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  font-weight: 800;
  letter-spacing: -1px;
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    font-size: 2.5rem;
  }
`;

const HeroSubtitle = styled(motion.p)`
  font-size: 1.5rem;
  color: ${props => props.theme.colors.text};
  margin-bottom: 2rem;
  max-width: 600px;
  line-height: 1.6;
  opacity: 0.9;
  position: relative;
  z-index: 1;
  
  @media (max-width: 768px) {
    font-size: 1.2rem;
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
  position: relative;
  z-index: 1;
  
  @media (max-width: 480px) {
    flex-direction: column;
  }
`;

const Button = styled(motion(Link))`
  padding: 1rem 2.5rem;
  font-size: 1.2rem;
  background: ${props => props.theme.colors.primary};
  color: ${props => props.theme.colors.background};
  border: none;
  border-radius: 50px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s ease;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  
  &:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
    background: ${props => props.theme.colors.accent};
  }
`;

const SecondaryButton = styled(Button)`
  background: transparent;
  border: 2px solid ${props => props.theme.colors.primary};
  color: ${props => props.theme.colors.primary};
  
  &:hover {
    background: ${props => props.theme.colors.primary};
    color: ${props => props.theme.colors.background};
  }
`;

const Hero: React.FC = () => {
  return (
    <HeroSection>
      <HeroTitle
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        Transform Your Body with Calisthenics
      </HeroTitle>
      <HeroSubtitle
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        Build strength, flexibility, and endurance using only your body weight. No equipment needed!
      </HeroSubtitle>
      <ButtonGroup>
        <Button
          to="/benefits"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.4 }}
        >
          Learn More
        </Button>
        <SecondaryButton
          to="/benefits"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.5 }}
        >
          View Benefits
        </SecondaryButton>
      </ButtonGroup>
    </HeroSection>
  );
};

export default Hero; 