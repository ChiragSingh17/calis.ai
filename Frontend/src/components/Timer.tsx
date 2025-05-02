import React, { useState, useEffect } from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';

const TimerSection = styled.section`
  padding: 3rem;
  text-align: center;
  background: ${props => props.theme.colors.background};
`;

const TimerTitle = styled.h2`
  font-size: 2rem;
  color: ${props => props.theme.colors.text};
  margin-bottom: 2rem;
`;

const TimeDisplay = styled(motion.div)`
  font-size: 4rem;
  color: ${props => props.theme.colors.primary};
  margin-bottom: 2rem;
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 1rem;
  justify-content: center;
`;

const Button = styled(motion.button)`
  padding: 0.8rem 1.5rem;
  font-size: 1rem;
  background: ${props => props.theme.colors.primary};
  color: ${props => props.theme.colors.background};
  border: none;
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: ${props => props.theme.colors.accent};
  }
`;

const Timer: React.FC = () => {
  const [time, setTime] = useState(0);
  const [isRunning, setIsRunning] = useState(false);

  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isRunning) {
      interval = setInterval(() => {
        setTime(prevTime => prevTime + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [isRunning]);

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <TimerSection>
      <TimerTitle>Live Workout Timer</TimerTitle>
      <TimeDisplay
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
        transition={{ duration: 0.3 }}
      >
        {formatTime(time)}
      </TimeDisplay>
      <ButtonGroup>
        <Button
          onClick={() => setIsRunning(!isRunning)}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          {isRunning ? 'Pause' : 'Start'}
        </Button>
        <Button
          onClick={() => {
            setTime(0);
            setIsRunning(false);
          }}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          Reset
        </Button>
      </ButtonGroup>
    </TimerSection>
  );
};

export default Timer; 