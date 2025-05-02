import React, { useEffect, useRef, useState } from 'react';
import styled from '@emotion/styled';
import { motion } from 'framer-motion';

const VideoContainer = styled.div`
  position: relative;
  width: 100%;
  max-width: 800px;
  margin: 0 auto;
  background: ${props => props.theme.colors.background};
  border: 2px solid ${props => props.theme.colors.primary};
  border-radius: 15px;
  overflow: hidden;
`;

const Video = styled.video`
  width: 100%;
  height: auto;
  display: block;
`;

const Canvas = styled.canvas`
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
`;

const Controls = styled.div`
  display: flex;
  gap: 1rem;
  justify-content: center;
  margin-top: 1rem;
`;

const Button = styled.button`
  padding: 0.8rem 1.5rem;
  background: ${props => props.theme.colors.primary};
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;

  &:hover {
    background: ${props => props.theme.colors.accent};
    transform: translateY(-2px);
  }
`;

const FeedbackContainer = styled.div`
  margin-top: 2rem;
  padding: 1.5rem;
  background: ${props => props.theme.colors.background};
  border: 2px solid ${props => props.theme.colors.primary};
  border-radius: 15px;
`;

const FeedbackTitle = styled.h3`
  color: ${props => props.theme.colors.text};
  margin-bottom: 1rem;
`;

const FeedbackList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
`;

const FeedbackItem = styled.li`
  color: ${props => props.theme.colors.text};
  margin-bottom: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;

  &::before {
    content: '•';
    color: ${props => props.theme.colors.primary};
  }
`;

const AnglesContainer = styled.div`
  margin-top: 1rem;
  padding: 1rem;
  background: ${props => props.theme.colors.background};
  border: 1px solid ${props => props.theme.colors.secondary};
  border-radius: 8px;
`;

const AngleItem = styled.div`
  color: ${props => props.theme.colors.text};
  margin-bottom: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const AngleLabel = styled.span`
  font-weight: 600;
`;

const AngleValue = styled.span`
  color: ${props => props.theme.colors.accent};
`;

interface ExerciseAnalyzerProps {
  exerciseType: 'pushup' | 'pullup' | 'squat';
}

interface Angles {
  [key: string]: number;
}

const ExerciseAnalyzer: React.FC<ExerciseAnalyzerProps> = ({ exerciseType }) => {
  const videoRef = useRef<HTMLVideoElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [feedback, setFeedback] = useState<string[]>([]);
  const [angles, setAngles] = useState<Angles>({});

  useEffect(() => {
    let stream: MediaStream | null = null;
    let animationFrameId: number;

    const startVideo = async () => {
      try {
        stream = await navigator.mediaDevices.getUserMedia({ video: true });
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error('Error accessing camera:', err);
      }
    };

    const sendFrameForAnalysis = async (frameData: string) => {
      try {
        const response = await fetch('http://localhost:5000/analyze', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ 
            frame: frameData,
            exerciseType: exerciseType
          }),
        });

        const data = await response.json();
        if (data.success) {
          setFeedback(data.feedback);
          setAngles(data.angles);
        }
      } catch (error) {
        console.error('Error analyzing frame:', error);
      }
    };

    const analyzeFrame = () => {
      if (!videoRef.current || !canvasRef.current || !isAnalyzing) return;

      const video = videoRef.current;
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');

      if (!ctx) return;

      // Set canvas dimensions to match video
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;

      // Draw video frame
      ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

      // Convert canvas to base64
      const frameData = canvas.toDataURL('image/jpeg').split(',')[1];
      
      // Send frame for analysis
      sendFrameForAnalysis(frameData);

      animationFrameId = requestAnimationFrame(analyzeFrame);
    };

    startVideo();

    if (isAnalyzing) {
      animationFrameId = requestAnimationFrame(analyzeFrame);
    }

    return () => {
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
      if (animationFrameId) {
        cancelAnimationFrame(animationFrameId);
      }
    };
  }, [isAnalyzing, exerciseType]);

  const toggleAnalysis = () => {
    setIsAnalyzing(!isAnalyzing);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <VideoContainer>
        <Video
          ref={videoRef}
          autoPlay
          playsInline
          muted
        />
        <Canvas ref={canvasRef} />
      </VideoContainer>
      
      <Controls>
        <Button onClick={toggleAnalysis}>
          {isAnalyzing ? 'Stop Analysis' : 'Start Analysis'}
        </Button>
      </Controls>

      {(feedback.length > 0 || Object.keys(angles).length > 0) && (
        <FeedbackContainer>
          <FeedbackTitle>Form Feedback</FeedbackTitle>
          <FeedbackList>
            {feedback.map((item, index) => (
              <FeedbackItem key={index}>{item}</FeedbackItem>
            ))}
          </FeedbackList>
          
          {Object.keys(angles).length > 0 && (
            <AnglesContainer>
              {Object.entries(angles).map(([key, value]) => (
                <AngleItem key={key}>
                  <AngleLabel>{key.replace('_', ' ').toUpperCase()}:</AngleLabel>
                  <AngleValue>{value.toFixed(1)}°</AngleValue>
                </AngleItem>
              ))}
            </AnglesContainer>
          )}
        </FeedbackContainer>
      )}
    </motion.div>
  );
};

export default ExerciseAnalyzer; 