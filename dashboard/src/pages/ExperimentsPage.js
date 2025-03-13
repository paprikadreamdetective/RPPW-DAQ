import React from 'react';
import './ExperimentsPage.css';
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faFlask, faVialCircleCheck, faXmarkCircle, faHourglass } from "@fortawesome/free-solid-svg-icons";
function ExperimentsPage() {
    
    return (
        <>
            <div className="experiments-page">
            <div className="exp-info">
          <p><strong>Experiments</strong> </p>
          
          <div className="exp-description"></div>
        </div>
    <div className="main">
      {/*<div className="searchbar2">
        <input type="text" name="" id="" placeholder="Search" />
        <div className="searchbtn">
          <img
            src="https://media.geeksforgeeks.org/wp-content/uploads/20221210180758/Untitled-design-(28).png"
            className="icn srchicn"
            alt="search-button"
          />
        </div>
      </div>*/}

      <div className="box-container">
        <div className="box box1">
          <div className="text">
            <h2 className="topic-heading">60.5k</h2>
            <h2 className="topic">Total experiments</h2>
          </div>
          {/*<img
            src="https://media.geeksforgeeks.org/wp-content/uploads/20221210184645/Untitled-design-(31).png"
            alt="Views"
          />*/}
          <FontAwesomeIcon icon={faFlask} size="2x" color="white"/> 
        </div>

        <div className="box box2">
          <div className="text">
            <h2 className="topic-heading">150</h2>
            <h2 className="topic">Active experiments</h2>
          </div>
          <FontAwesomeIcon icon={faHourglass} size="2x" color="white"/> 
        </div>

        <div className="box box3">
          <div className="text">
            <h2 className="topic-heading">320</h2>
            <h2 className="topic">Experiments interrupted</h2>
          </div>
          <FontAwesomeIcon icon={faXmarkCircle} size="2x" color="white"/> 
        </div>

        <div className="box box4">
          <div className="text">
            <h2 className="topic-heading">70</h2>
            <h2 className="topic">Experiments completed</h2>
          </div>
          <FontAwesomeIcon icon={faVialCircleCheck} size="2x" color="white"/> 
        </div>
      </div>

      <div className="report-container">
        <div className="report-header">
          <h1 className="recent-Articles">Recent Experiments</h1>
          <button className="view">View All</button>
        </div>

        <div className="report-body">
          <div className="report-topic-heading">
            <h3 className="t-op">Experiment</h3>
            <h3 className="t-op">Duration</h3>
            <h3 className="t-op">Description</h3>
            <h3 className="t-op">Status</h3>
          </div>

          <div className="items">
            <div className="item1">
              <h3 className="t-op-nextlvl">Article 73</h3>
              <h3 className="t-op-nextlvl">2.9k</h3>
              <h3 className="t-op-nextlvl">210</h3>
              <h3 className="t-op-nextlvl label-tag">Published</h3>
            </div>

            <div className="item1">
              <h3 className="t-op-nextlvl">Article 72</h3>
              <h3 className="t-op-nextlvl">1.5k</h3>
              <h3 className="t-op-nextlvl">360</h3>
              <h3 className="t-op-nextlvl label-tag">Published</h3>
            </div>

            <div className="item1">
              <h3 className="t-op-nextlvl">Article 71</h3>
              <h3 className="t-op-nextlvl">1.1k</h3>
              <h3 className="t-op-nextlvl">150</h3>
              <h3 className="t-op-nextlvl label-tag">Published</h3>
            </div>

            <div className="item1">
              <h3 className="t-op-nextlvl">Article 70</h3>
              <h3 className="t-op-nextlvl">1.2k</h3>
              <h3 className="t-op-nextlvl">420</h3>
              <h3 className="t-op-nextlvl label-tag">Published</h3>
            </div>

            <div className="item1">
              <h3 className="t-op-nextlvl">Article 69</h3>
              <h3 className="t-op-nextlvl">2.6k</h3>
              <h3 className="t-op-nextlvl">190</h3>
              <h3 className="t-op-nextlvl label-tag">Published</h3>
            </div>

            <div className="item1">
              <h3 className="t-op-nextlvl">Article 68</h3>
              <h3 className="t-op-nextlvl">1.9k</h3>
              <h3 className="t-op-nextlvl">390</h3>
              <h3 className="t-op-nextlvl label-tag">Published</h3>
            </div>

            <div className="item1">
              <h3 className="t-op-nextlvl">Article 67</h3>
              <h3 className="t-op-nextlvl">1.2k</h3>
              <h3 className="t-op-nextlvl">580</h3>
              <h3 className="t-op-nextlvl label-tag">Published</h3>
            </div>

            <div className="item1">
              <h3 className="t-op-nextlvl">Article 66</h3>
              <h3 className="t-op-nextlvl">3.6k</h3>
              <h3 className="t-op-nextlvl">160</h3>
              <h3 className="t-op-nextlvl label-tag">Published</h3>
            </div>

            <div className="item1">
              <h3 className="t-op-nextlvl">Article 65</h3>
              <h3 className="t-op-nextlvl">1.3k</h3>
              <h3 className="t-op-nextlvl">220</h3>
              <h3 className="t-op-nextlvl label-tag">Published</h3>
            </div>
          </div>
        </div>
      </div>
    </div>


            </div>
        </>
    )
}
export default ExperimentsPage;