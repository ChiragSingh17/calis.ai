import React from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';
import { Link, useLocation } from 'react-router-dom';

const NavContainer = styled.nav`
  position: sticky;
  top: 0;
  background: ${props => props.theme.colors.background};
  padding: 1rem 2rem;
  z-index: 1000;
  border-bottom: 2px solid ${props => props.theme.colors.primary};
`;

const NavList = styled.ul`
  display: flex;
  justify-content: center;
  gap: 2rem;
  list-style: none;
  margin: 0;
  padding: 0;
  
  @media (max-width: 768px) {
    flex-direction: column;
    align-items: center;
    gap: 1rem;
  }
`;

const NavItem = styled.li`
  position: relative;
`;

const NavLink = styled(Link)<{ isActive: boolean }>`
  color: ${props => props.isActive ? props.theme.colors.primary : props.theme.colors.text};
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  padding: 0.5rem 1rem;
  border-radius: 30px;
  transition: all 0.3s ease;
  
  &:hover {
    color: ${props => props.theme.colors.primary};
    background: rgba(0, 168, 255, 0.1);
  }
`;

const ActiveIndicator = styled(motion.div)`
  position: absolute;
  bottom: -2px;
  left: 0;
  right: 0;
  height: 2px;
  background: ${props => props.theme.colors.primary};
`;

const Navigation: React.FC = () => {
  const location = useLocation();

  return (
    <NavContainer>
      <NavList>
        <NavItem>
          <NavLink to="/" isActive={location.pathname === '/'}>
            Home
          </NavLink>
          {location.pathname === '/' && (
            <ActiveIndicator
              layoutId="activeIndicator"
              initial={false}
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
            />
          )}
        </NavItem>
        <NavItem>
          <NavLink to="/workouts" isActive={location.pathname === '/workouts'}>
            Workouts
          </NavLink>
          {location.pathname === '/workouts' && (
            <ActiveIndicator
              layoutId="activeIndicator"
              initial={false}
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
            />
          )}
        </NavItem>
        <NavItem>
          <NavLink to="/progress" isActive={location.pathname === '/progress'}>
            Progress
          </NavLink>
          {location.pathname === '/progress' && (
            <ActiveIndicator
              layoutId="activeIndicator"
              initial={false}
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
            />
          )}
        </NavItem>
        <NavItem>
          <NavLink to="/community" isActive={location.pathname === '/community'}>
            Community
          </NavLink>
          {location.pathname === '/community' && (
            <ActiveIndicator
              layoutId="activeIndicator"
              initial={false}
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
            />
          )}
        </NavItem>
        <NavItem>
          <NavLink to="/benefits" isActive={location.pathname === '/benefits'}>
            Benefits
          </NavLink>
          {location.pathname === '/benefits' && (
            <ActiveIndicator
              layoutId="activeIndicator"
              initial={false}
              transition={{ type: "spring", stiffness: 500, damping: 30 }}
            />
          )}
        </NavItem>
      </NavList>
    </NavContainer>
  );
};

export default Navigation; 