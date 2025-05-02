import React from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';

const WorkoutsContainer = styled.div`
  padding: 4rem 2rem;
  background: ${props => props.theme.colors.background};
  min-height: 100vh;
`;

const Title = styled(motion.h1)`
  font-size: 3rem;
  color: ${props => props.theme.colors.text};
  text-align: center;
  margin-bottom: 3rem;
`;

const WorkoutGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const WorkoutCard = styled(motion.div)`
  background: ${props => props.theme.colors.background};
  border: 2px solid ${props => props.theme.colors.primary};
  border-radius: 15px;
  padding: 2rem;
  color: ${props => props.theme.colors.text};
  transition: all 0.3s ease;
  cursor: pointer;
  
  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  }
`;

const WorkoutTitle = styled.h3`
  font-size: 1.5rem;
  color: ${props => props.theme.colors.primary};
  margin-bottom: 1rem;
`;

const WorkoutDescription = styled.p`
  color: ${props => props.theme.colors.text};
  opacity: 0.8;
  line-height: 1.6;
  margin-bottom: 1.5rem;
`;

const DifficultyBadge = styled.span<{ difficulty: 'Beginner' | 'Intermediate' | 'Advanced' }>`
  display: inline-block;
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  background: ${props => {
    switch (props.difficulty) {
      case 'Beginner':
        return '#00b894';
      case 'Intermediate':
        return '#fdcb6e';
      case 'Advanced':
        return '#d63031';
      default:
        return props.theme.colors.primary;
    }
  }};
  color: white;
`;

const DurationText = styled.span`
  color: ${props => props.theme.colors.text};
  opacity: 0.7;
`;

const workouts = [
  {
    title: 'Push-Up Progression',
    description: 'Master the art of push-ups with our step-by-step progression program. Perfect for building upper body strength.',
    difficulty: 'Beginner',
    duration: '4 weeks'
  },
  {
    title: 'Pull-Up Mastery',
    description: 'Learn proper pull-up form and build the strength needed to perform this fundamental exercise.',
    difficulty: 'Intermediate',
    duration: '6 weeks'
  },
  {
    title: 'Handstand Training',
    description: 'Develop balance and core strength with our comprehensive handstand training program.',
    difficulty: 'Advanced',
    duration: '8 weeks'
  },
  {
    title: 'Muscle-Up Progression',
    description: 'Combine strength and technique to master the muscle-up, one of the most impressive calisthenics moves.',
    difficulty: 'Advanced',
    duration: '10 weeks'
  },
  {
    title: 'Core Strength Fundamentals',
    description: 'Build a strong core foundation with our beginner-friendly core workout program.',
    difficulty: 'Beginner',
    duration: '4 weeks'
  },
  {
    title: 'Leg Strength & Mobility',
    description: 'Develop powerful legs and improve mobility with our specialized leg training program.',
    difficulty: 'Intermediate',
    duration: '6 weeks'
  }
];

const Workouts: React.FC = () => {
  return (
    <WorkoutsContainer>
      <Title
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        Workout Programs
      </Title>
      <WorkoutGrid>
        {workouts.map((workout, index) => (
          <WorkoutCard
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            whileHover={{ scale: 1.02 }}
          >
            <WorkoutTitle>{workout.title}</WorkoutTitle>
            <WorkoutDescription>{workout.description}</WorkoutDescription>
            <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
              <DifficultyBadge difficulty={workout.difficulty as 'Beginner' | 'Intermediate' | 'Advanced'}>
                {workout.difficulty}
              </DifficultyBadge>
              <DurationText>{workout.duration}</DurationText>
            </div>
          </WorkoutCard>
        ))}
      </WorkoutGrid>
    </WorkoutsContainer>
  );
};

export default Workouts; 