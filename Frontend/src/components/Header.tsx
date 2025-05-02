import React from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';

const HeaderContainer = styled.header`
  text-align: center;
  padding: 2rem;
  background: ${props => props.theme.colors.background};
`;

const Title = styled(motion.h1)`
  font-size: 3rem;
  color: ${props => props.theme.colors.text};
  margin-bottom: 1rem;
  font-weight: 800;
`;

const Subtitle = styled(motion.p)`
  font-size: 1.2rem;
  color: ${props => props.theme.colors.text};
  opacity: 0.8;
`;

const Header: React.FC = () => {
  return (
    <HeaderContainer>
      <Title
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        Calisthenics Aesthetics
      </Title>
      <Subtitle
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, delay: 0.2 }}
      >
        Unleash Your True Potential
      </Subtitle>
    </HeaderContainer>
  );
};

export default Header; 