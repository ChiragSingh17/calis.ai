import React, { useState } from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import ExerciseAnalyzer from '../components/ExerciseAnalyzer';

const ProgressContainer = styled.div`
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

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto 3rem;
`;

const StatCard = styled(motion.div)`
  background: ${props => props.theme.colors.background};
  border: 2px solid ${props => props.theme.colors.primary};
  border-radius: 15px;
  padding: 2rem;
  text-align: center;
`;

const StatValue = styled.div`
  font-size: 2.5rem;
  color: ${props => props.theme.colors.primary};
  font-weight: 800;
  margin-bottom: 0.5rem;
`;

const StatLabel = styled.div`
  color: ${props => props.theme.colors.text};
  opacity: 0.8;
  font-size: 1.1rem;
`;

const ProgressSection = styled.section`
  max-width: 1200px;
  margin: 0 auto;
  background: ${props => props.theme.colors.background};
  border: 2px solid ${props => props.theme.colors.primary};
  border-radius: 15px;
  padding: 2rem;
  margin-bottom: 2rem;
`;

const SectionTitle = styled.h2`
  color: ${props => props.theme.colors.text};
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
`;

const ProgressBar = styled.div<{ progress: number }>`
  height: 20px;
  background: ${props => props.theme.colors.background};
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 1rem;
  
  &::before {
    content: '';
    display: block;
    height: 100%;
    width: ${props => props.progress}%;
    background: ${props => props.theme.colors.primary};
    transition: width 0.5s ease;
  }
`;

const ProgressLabel = styled.div`
  display: flex;
  justify-content: space-between;
  color: ${props => props.theme.colors.text};
  opacity: 0.8;
`;

const AchievementText = styled.div`
  color: ${props => props.theme.colors.text};
  opacity: 0.8;
`;

const ExerciseSection = styled.section`
  max-width: 1200px;
  margin: 2rem auto;
  background: ${props => props.theme.colors.background};
  border: 2px solid ${props => props.theme.colors.primary};
  border-radius: 15px;
  padding: 2rem;
`;

const ExerciseSelector = styled.div`
  display: flex;
  gap: 1rem;
  margin-bottom: 2rem;
`;

const ExerciseButton = styled.button<{ isActive: boolean }>`
  padding: 0.8rem 1.5rem;
  background: ${props => props.isActive ? props.theme.colors.primary : 'transparent'};
  color: ${props => props.isActive ? 'white' : props.theme.colors.text};
  border: 2px solid ${props => props.theme.colors.primary};
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;

  &:hover {
    background: ${props => props.theme.colors.primary};
    color: white;
  }
`;

const stats = [
  { label: 'Total Workouts', value: '42' },
  { label: 'Current Streak', value: '7 days' },
  { label: 'Total Time', value: '28h 15m' },
  { label: 'Calories Burned', value: '12,450' }
];

const progressData = [
  { label: 'Push-Ups', progress: 75 },
  { label: 'Pull-Ups', progress: 60 },
  { label: 'Squats', progress: 90 },
  { label: 'Plank', progress: 85 }
];

const Progress: React.FC = () => {
  const [selectedExercise, setSelectedExercise] = useState<'pushup' | 'pullup' | 'squat'>('pushup');

  return (
    <ProgressContainer>
      <Title
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        Your Progress
      </Title>
      
      <StatsGrid>
        {stats.map((stat, index) => (
          <StatCard
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <StatValue>{stat.value}</StatValue>
            <StatLabel>{stat.label}</StatLabel>
          </StatCard>
        ))}
      </StatsGrid>

      <ExerciseSection>
        <SectionTitle>Exercise Analysis</SectionTitle>
        <ExerciseSelector>
          <ExerciseButton
            isActive={selectedExercise === 'pushup'}
            onClick={() => setSelectedExercise('pushup')}
          >
            Push-Ups
          </ExerciseButton>
          <ExerciseButton
            isActive={selectedExercise === 'pullup'}
            onClick={() => setSelectedExercise('pullup')}
          >
            Pull-Ups
          </ExerciseButton>
          <ExerciseButton
            isActive={selectedExercise === 'squat'}
            onClick={() => setSelectedExercise('squat')}
          >
            Squats
          </ExerciseButton>
        </ExerciseSelector>
        <ExerciseAnalyzer exerciseType={selectedExercise} />
      </ExerciseSection>

      <ProgressSection>
        <SectionTitle>Exercise Progress</SectionTitle>
        {progressData.map((item, index) => (
          <div key={index} style={{ marginBottom: '1.5rem' }}>
            <ProgressLabel>
              <span>{item.label}</span>
              <span>{item.progress}%</span>
            </ProgressLabel>
            <ProgressBar progress={item.progress} />
          </div>
        ))}
      </ProgressSection>

      <ProgressSection>
        <SectionTitle>Recent Achievements</SectionTitle>
        <AchievementText>
          <p>✅ Completed 30-day push-up challenge</p>
          <p>✅ Achieved 10 consecutive pull-ups</p>
          <p>✅ Held a 2-minute plank</p>
        </AchievementText>
      </ProgressSection>
    </ProgressContainer>
  );
};

export default Progress; 