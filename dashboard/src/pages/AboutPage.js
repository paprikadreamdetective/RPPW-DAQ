import './AboutPage.css';

function AboutPage() {
    return (
        <div className="about-page">
            <div className="about-info">
                <p><strong>About BioReactify</strong></p>
                <div className="about-description">
                    <p>
                        BioReactify is an open-source project that defines a distributed monitoring system architecture. 
                        Designed for flexibility, it can be adapted for various applications, from industrial monitoring 
                        to scientific research. By leveraging IoT technologies, BioReactify enables real-time data acquisition 
                        and remote management of sensors and actuators.
                    </p>
                </div>
            </div>
        </div>
    );
}

export default AboutPage;
