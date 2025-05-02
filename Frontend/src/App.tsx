import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled from '@emotion/styled';
import { ThemeProvider } from '@emotion/react';
import theme from './theme';
import Header from './components/Header';
import Hero from './components/Hero';
import Timer from './components/Timer';
import Benefits from './pages/Benefits';
import Workouts from './pages/Workouts';
import Progress from './pages/Progress';
import Community from './pages/Community';
import Navigation from './components/Navigation';

const AppContainer = styled.div`
  min-height: 100vh;
  background: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text};
`;

const HomePage = () => (
  <>
    <Hero />
    <Timer />
  </>
);

const App: React.FC = () => {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <AppContainer>
          <Header />
          <Navigation />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/workouts" element={<Workouts />} />
            <Route path="/progress" element={<Progress />} />
            <Route path="/community" element={<Community />} />
            <Route path="/benefits" element={<Benefits />} />
          </Routes>
        </AppContainer>
      </Router>
    </ThemeProvider>
  );
};

export default App; 