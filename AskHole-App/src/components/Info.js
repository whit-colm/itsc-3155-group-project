import React from 'react';
import '../App.css';
import './Info.css';

const Info = () => {
  const frontendTeam = [
    {
      name: 'John Doe',
      role: 'Front-end Developer',
      image: '/images/john.jpg',
    },
    {
      name: 'Jane Smith',
      role: 'Front-end Developer',
      image: '/images/jane.jpg',
    },
    {
      name: 'Alex Johnson',
      role: 'Front-end Developer',
      image: '/images/alex.jpg',
    },
  ];

  const backendTeam = [
    {
      name: 'Sarah Brown',
      role: 'Back-end Developer',
      image: '/images/sarah.jpg',
    },
    {
      name: 'Mike Davis',
      role: 'Back-end Developer',
      image: '/images/mike.jpg',
    },
    {
      name: 'Emily White',
      role: 'Back-end Developer',
      image: '/images/emily.jpg',
    },
    {
      name: 'David Wilson',
      role: 'Back-end Developer',
      image: '/images/david.jpg',
    },
    {
      name: 'Grace Lee',
      role: 'Back-end Developer',
      image: '/images/grace.jpg',
    },
  ];

  return (
    <div className='info-container'>
      <video src='/video/CollegeSockFootage.mp4' autoPlay loop muted />

      <div className='text-content'>
        <h1>Meet Our Front-end Team</h1>
        <div className='team'>
          {frontendTeam.map((member, index) => (
            <div className='member-profile' key={index}>
              <img src={member.image} alt={member.name} />
              <h3>{member.name}</h3>
              <p>{member.role}</p>
            </div>
          ))}
        </div>

        <h1>Meet Our Back-end Team</h1>
        <div className='team'>
          {backendTeam.map((member, index) => (
            <div className='member-profile' key={index}>
              <img src={member.image} alt={member.name} />
              <h3>{member.name}</h3>
              <p>{member.role}</p>
            </div>
          ))}
        </div>

        <h1 className='project-mission'>Our Project Mission</h1>
        <p className='project-mission-text'>Deliver innovative solutions that exceed expectations and make a positive impact for our clients.</p>
      </div>
    </div>
  );
}

export default Info;