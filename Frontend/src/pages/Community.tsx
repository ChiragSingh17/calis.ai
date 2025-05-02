import React from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';

const CommunityContainer = styled.div`
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

const PostGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
`;

const PostCard = styled(motion.div)`
  background: ${props => props.theme.colors.background};
  border: 2px solid ${props => props.theme.colors.primary};
  border-radius: 15px;
  padding: 2rem;
  color: ${props => props.theme.colors.text};
`;

const PostHeader = styled.div`
  display: flex;
  align-items: center;
  margin-bottom: 1rem;
`;

const Avatar = styled.div`
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: ${props => props.theme.colors.primary};
  margin-right: 1rem;
`;

const UserInfo = styled.div`
  flex: 1;
`;

const Username = styled.div`
  font-weight: 600;
  color: ${props => props.theme.colors.text};
`;

const PostTime = styled.div`
  font-size: 0.8rem;
  color: ${props => props.theme.colors.text};
  opacity: 0.6;
`;

const PostContent = styled.div`
  margin-bottom: 1.5rem;
  line-height: 1.6;
`;

const PostImage = styled.img`
  width: 100%;
  border-radius: 10px;
  margin-bottom: 1rem;
`;

const PostActions = styled.div`
  display: flex;
  gap: 1rem;
  color: ${props => props.theme.colors.text};
  opacity: 0.8;
`;

const ActionButton = styled.button`
  background: none;
  border: none;
  color: ${props => props.theme.colors.text};
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  opacity: 0.8;
  transition: opacity 0.3s ease;
  
  &:hover {
    opacity: 1;
  }
`;

const posts = [
  {
    username: 'FitnessEnthusiast',
    time: '2 hours ago',
    content: 'Just completed my first muscle-up! After 3 months of training, the hard work finally paid off. 💪',
    image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
    likes: 42,
    comments: 8
  },
  {
    username: 'CalisthenicsPro',
    time: '5 hours ago',
    content: 'Sharing my new handstand progression routine. Perfect for beginners looking to build strength and balance.',
    image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
    likes: 78,
    comments: 15
  },
  {
    username: 'StreetWorkout',
    time: '1 day ago',
    content: '30-day push-up challenge completed! Started with 10, now doing 50 in a row. Consistency is key!',
    image: 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80',
    likes: 95,
    comments: 23
  }
];

const Community: React.FC = () => {
  return (
    <CommunityContainer>
      <Title
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
      >
        Community
      </Title>
      <PostGrid>
        {posts.map((post, index) => (
          <PostCard
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <PostHeader>
              <Avatar />
              <UserInfo>
                <Username>{post.username}</Username>
                <PostTime>{post.time}</PostTime>
              </UserInfo>
            </PostHeader>
            <PostContent>{post.content}</PostContent>
            <PostImage src={post.image} alt="Post content" />
            <PostActions>
              <ActionButton>
                <span>❤️</span>
                <span>{post.likes}</span>
              </ActionButton>
              <ActionButton>
                <span>💬</span>
                <span>{post.comments}</span>
              </ActionButton>
              <ActionButton>
                <span>🔄</span>
                <span>Share</span>
              </ActionButton>
            </PostActions>
          </PostCard>
        ))}
      </PostGrid>
    </CommunityContainer>
  );
};

export default Community; 