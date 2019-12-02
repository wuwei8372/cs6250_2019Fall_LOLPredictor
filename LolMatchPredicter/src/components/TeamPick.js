import React, { Component } from 'react';
import '../css/TeamPick.css';
import heroBigData from '../heromap/bigDataResult.json';
import hero from '../heromap/hero.json';
class TeamPick extends Component {
    
  render() {
    let myTeamList = this.props.myTeamHeroes;
    let opponentTeamList = this.props.opponentTeamHeroes;

    let myTeamnames = myTeamList.map( (name, index) => {
        const style = {border: '3px solid transparent'}
        const divstyle = {display: "inline-block"}
        const figcapstyle = {textAlign: 'center', color: "red", fontSize: "20px", fontWeight: "bold"}
        let curtName = {name}.name.toString()
        let heroName = curtName.substring(0,curtName.length - 4)
        let heroIndex = hero[heroName].key;
        let usageRate = "usage rate is: " + heroBigData[heroIndex].usage_rate 
        let winRate = "win rate is: " + heroBigData[heroIndex].win_rate
        let topTeammates = "Top teamates: " + "\n" + heroBigData[heroIndex].top_teammates
        let titleName = heroName + "\n" + usageRate + "\n" + winRate + "\n" + topTeammates
        // console.log(curtName)
        return (
                <div style={divstyle}>
                  <img key={index} 
                      style={style} 
                      title= {titleName}
                      className="img-responsive" alt="" 
                      src={require(`../images/heros/${name}`)} />
                  <figcaption style={figcapstyle}> {heroName}</figcaption>
                </div>
        )
    } );
    let opponentTeamNames = opponentTeamList.map( (name, index) => {
        const style = {border: '3px solid transparent'}
        const divstyle = {display: "inline-block"}
        const figcapstyle = {textAlign: 'center', color: "red", fontSize: "20px", fontWeight: "bold"}
        let curtName = {name}.name.toString()
        let heroName = curtName.substring(0,curtName.length - 4)
        let heroIndex = hero[heroName].key;
        let usageRate = "usage rate is: " + heroBigData[heroIndex].usage_rate 
        let winRate = "win rate is: " + heroBigData[heroIndex].win_rate
        let topTeammates = "Top teamates: " + "\n" + heroBigData[heroIndex].top_teammates
        let titleName = heroName + "\n" + usageRate + "\n" + winRate + "\n" + topTeammates
        // console.log(curtName)
        return (
                <div style={divstyle}>
                  <img key={index} 
                      style={style} 
                      title= {titleName}
                      className="img-responsive" alt="" 
                      src={require(`../images/heros/${name}`)} />
                  <figcaption style={figcapstyle}> {heroName}</figcaption>
                </div>
        )
    } );

    const buttonStyle = {fontSize: '30px'}
    return (
      
    <div className="TeamPick">

        <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6">
            <h1> My Team picks:</h1>
            { myTeamnames }
        </div>
        <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6">
            <h1> Opponent Team picks:</h1>
            { opponentTeamNames }
        </div>
        <div>
             <button onClick={this.props.handleDeleteHero} style={buttonStyle}>
                Re-do the last hero selection
            </button>
        </div>
    
    </div>
    );
  }
}

export default TeamPick;