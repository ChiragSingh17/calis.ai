import React from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';

const BenefitsContainer = styled.div`
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const BenefitsTitle = styled.h1`
  text-align: center;
  font-size: 2.5rem;
  margin-bottom: 3rem;
  color: ${props => props.theme.colors.text};
`;

const BenefitsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
`;

const BenefitCard = styled(motion.div)`
  background: ${props => props.theme.colors.background};
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;

  &:hover {
    transform: translateY(-5px);
  }
`;

const BenefitIcon = styled.div`
  font-size: 2.5rem;
  margin-bottom: 1rem;
  color: ${props => props.theme.colors.primary};
`;

const BenefitTitle = styled.h3`
  font-size: 1.5rem;
  margin-bottom: 1rem;
  color: ${props => props.theme.colors.text};
`;

const BenefitDescription = styled.p`
  color: ${props => props.theme.colors.text};
  line-height: 1.6;
`;

const benefits = [
  {
    icon: '💪',
    title: 'Strength Building',
    description: 'Build functional strength using your body weight. Perfect for developing core stability and muscle endurance.'
  },
  {
    icon: '🧘',
    title: 'Flexibility',
    description: 'Improve your range of motion and flexibility through controlled movements and proper form.'
  },
  {
    icon: '🏃',
    title: 'Endurance',
    description: 'Enhance your cardiovascular health and stamina with high-intensity calisthenics workouts.'
  },
  {
    icon: '🧠',
    title: 'Mental Focus',
    description: 'Develop mental discipline and focus through challenging bodyweight exercises and progressions.'
  },
  {
    icon: '⚡',
    title: 'Explosive Power',
    description: 'Train for explosive movements and dynamic strength through plyometric exercises.'
  },
  {
    icon: '🔄',
    title: 'Versatility',
    description: 'Workout anywhere, anytime with minimal equipment. Perfect for home workouts or outdoor training.'
  }
];

const Benefits: React.FC = () => {
  return (
    <BenefitsContainer>
      <BenefitsTitle>Benefits of Calisthenics</BenefitsTitle>
      <BenefitsGrid>
        {benefits.map((benefit, index) => (
          <BenefitCard
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <BenefitIcon>{benefit.icon}</BenefitIcon>
            <BenefitTitle>{benefit.title}</BenefitTitle>
            <BenefitDescription>{benefit.description}</BenefitDescription>
          </BenefitCard>
        ))}
      </BenefitsGrid>
    </BenefitsContainer>
  );
};

export default Benefits; 