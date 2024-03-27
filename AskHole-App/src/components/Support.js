import React from 'react';
import '../App.css';
import './Support.css';

function Support() {
  return (
    <div class="hero-container">
        <video src='/video/SupportVideo.mp4' autoPlay loop muted />
        <div className="heading-container">
            <h1>Supporting Our Users</h1>
            <p>AskHole's mission statement is to take away much of the barriers that get in the way of learning as possible. To hold to this mission we wish to have a robust support structure in place so that any difficuties or issues with our platform can be addressed quickly and efficiently.</p>
        </div>
        <div class="support-container">
            <div class="box">
                <h1>Developer Team</h1>
                <p>
                    If you ever run into a technical issue involving our platform, please contact one of our developer team representatives
                    so that we can resolve this issue. you can contact us at : askholedev@gmail.com or join our Discord server by clicking on the button below.
                    You can also  reach out to our developer team directly through GitHub by clicking on the GitHub icon below.
                </p>
            </div>
            <div class="box">
                <h1>Business Team</h1>
                <p>If you would like to contribute to our work and cause, feel free to reach to our business team either at: askholebusiness@gmail.com or by joining our Discord by clicking on the icon below.</p>
            </div>
        </div>
    </div>
  );
}

export default Support;