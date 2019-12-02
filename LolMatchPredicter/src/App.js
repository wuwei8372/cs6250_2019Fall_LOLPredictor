import React, { Component } from 'react';
import './css/App.css';
import Background from './images/background.jpg';
import TeamPick from './components/TeamPick';
import Result from './components/Result';
import HeroPicker from './components/HeroPikcer';
import hero from './heromap/hero.json';
import heroBigData from './heromap/bigDataResult.json';

const FILE_NAMES = ["Aatrox.png","Ahri.png","Akali.png","Alistar.png","Amumu.png","Anivia.png","Annie.png","Ashe.png","AurelionSol.png","Azir.png","Bard.png","Blitzcrank.png","Brand.png","Braum.png","Caitlyn.png","Camille.png","Cassiopeia.png","Chogath.png","Corki.png","Darius.png","Diana.png","DrMundo.png","Draven.png","Ekko.png","Elise.png","Evelynn.png","Ezreal.png","Fiddlesticks.png","Fiora.png","Fizz.png","Galio.png","Gangplank.png","Garen.png","Gnar.png","Gragas.png","Graves.png","Hecarim.png","Heimerdinger.png","Illaoi.png","Irelia.png","Ivern.png","Janna.png","JarvanIV.png","Jax.png","Jayce.png","Jhin.png","Jinx.png","Kaisa.png","Kalista.png","Karma.png","Karthus.png","Kassadin.png","Katarina.png","Kayle.png","Kayn.png","Kennen.png","Khazix.png","Kindred.png","Kled.png","KogMaw.png","Leblanc.png","LeeSin.png","Leona.png","Lissandra.png","Lucian.png","Lulu.png","Lux.png","Malphite.png","Malzahar.png","Maokai.png","MasterYi.png","MissFortune.png","MonkeyKing.png","Mordekaiser.png","Morgana.png","Nami.png","Nasus.png","Nautilus.png","Neeko.png","Nidalee.png","Nocturne.png","Nunu.png","Olaf.png","Orianna.png","Ornn.png","Pantheon.png","Poppy.png","Pyke.png","Qiyana.png","Quinn.png","Rakan.png","Rammus.png","RekSai.png","Renekton.png","Rengar.png","Riven.png","Rumble.png","Ryze.png","Sejuani.png","Senna.png","Shaco.png","Shen.png","Shyvana.png","Singed.png","Sion.png","Sivir.png","Skarner.png","Sona.png","Soraka.png","Swain.png","Sylas.png","Syndra.png","TahmKench.png","Taliyah.png","Talon.png","Taric.png","Teemo.png","Thresh.png","Tristana.png","Trundle.png","Tryndamere.png","TwistedFate.png","Twitch.png","Udyr.png","Urgot.png","Varus.png","Vayne.png","Veigar.png","Velkoz.png","Vi.png","Viktor.png","Vladimir.png","Volibear.png","Warwick.png","Xayah.png","Xerath.png","XinZhao.png","Yasuo.png","Yorick.png","Yuumi.png","Zac.png","Zed.png","Ziggs.png","Zilean.png","Zoe.png","Zyra.png"];
var backgroundStyle = {
  width: "100%",
  height: "100%",
  backgroundPosition: 'center',
  backgroundSize: 'cover',
  backgroundImage: `url(${Background})`,
};

class App extends Component {
  constructor(props) {
    super(props)
    let images = FILE_NAMES.map( (name, index) => {
      const style = {border: '3px solid transparent'}
      const divstyle = {display: "inline-block"}
      const figcapstyle = {textAlign: 'center', color: "white", fontSize: "20px", fontWeight: "bold"}
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
                    onClick={this.handleClickImage.bind(this, {name})} 
                    className="img-responsive" alt="" 
                    src={require(`./images/heros/${name}`)} />
                <figcaption style={figcapstyle}> {heroName}</figcaption>
              </div>
      )
    });
    this.state = {
        myTeamHeroes: [],
        opponentTeamHeroes: [],
        round: 1,
        images: images,
        tier: 36,
        favoriteHero: "puck"
    }
    this.ShowRecommendedHeroes = this.ShowRecommendedHeroes.bind(this);
  }

  handleClickImage = (dataFromHeroPicker) => {
    let curtRound = this.state.round;
    let newMyTeamHeroes = this.state.myTeamHeroes;
    let newOpponentHeroes = this.state.opponentTeamHeroes;
    if (newMyTeamHeroes.length < 5 && (curtRound === 1 || curtRound === 4 || curtRound === 5 || curtRound === 8 || curtRound === 9)) {
      if (!newOpponentHeroes.includes(dataFromHeroPicker.name) && !newMyTeamHeroes.includes(dataFromHeroPicker.name)) {
        newMyTeamHeroes.push(dataFromHeroPicker.name);
        curtRound+=1;
      }
    } else if (newOpponentHeroes.length < 5 && (curtRound === 2 || curtRound === 3 || curtRound === 6 || curtRound === 7 || curtRound === 10)) {
      if (!newOpponentHeroes.includes(dataFromHeroPicker.name) && !newMyTeamHeroes.includes(dataFromHeroPicker.name)) {
        newOpponentHeroes.push(dataFromHeroPicker.name);
        curtRound+=1;
      }
    }
    this.setState({myTeamHeroes : newMyTeamHeroes});
    this.setState({opponentTeamHeroes : newOpponentHeroes});
    this.setState({round : curtRound});
    // console.log(this.state.myTeamHeroes);
  };
  resetTeamPick = () => {
    this.setState({myTeamHeroes: []});
    this.setState({opponentTeamHeroes: []});
    this.setState({round: 1})
  }
  convertIdsToFileNames = (passedRecommendedHeroesIds) => {
    let passedRecommendedHeroesImages = []
    for (let i = 0; i < passedRecommendedHeroesIds.length; i++) {
      let curtId = passedRecommendedHeroesIds[i];
      // find hero name by id
      // console.log(curtId)
      var formattedTargetName = "";
      // console.log(curtId)
      for (let curthero in hero) {
        var targetName = hero[curthero].localized_name;
        // console.log(hero[curthero].id)
        if (curtId === hero[curthero].id) {
          for (let i = 0; i < targetName.length; i++) {   
            if (targetName.charAt(i).toLowerCase() === '-') {
                formattedTargetName += ' ';
            } else if (targetName.charAt(i).toLowerCase() === '\'') {
                continue;
            } else {
                formattedTargetName += targetName.charAt(i).toLowerCase();
            }
          }
        }
      }
      // console.log(formattedTargetName)
      // find file name by hero name
      
      for (let j = 0; j < FILE_NAMES.length; j++) {
        let finalName = "";
        let oriName = FILE_NAMES[j].split(".")[0];
        // console.log(oriName);
        
        for (let k = 0; k < oriName.length; k++) {
            if (oriName.charAt(k) === '_') {
                finalName += ' ';
            } else {
                finalName += oriName.charAt(k).toLowerCase();
            }
        }
        // console.log(finalName)
        if (finalName == formattedTargetName) {
          passedRecommendedHeroesImages.push(FILE_NAMES[j]);
          break;
        }
      }
    }
    // console.log(passedRecommendedHeroesImages)
    return passedRecommendedHeroesImages;
  }
  async ShowRecommendedHeroes() {
    // console.log(this.state.myTeamHeroes)
      // do http call here and use this.state.tier and this.state.favoriteHero as input, get a list of array as output which is passedRecommendedHeroesIds
    // let curtTier = this.state.tier;
    // let curtId = this.state.id
    const response = await fetch(
      //   `${uriBase}?visualFeatures=${visualFeatures}&details=${details}&language=${language}`,
      `http://localhost:5000/recommend`,
        {
          method: 'post',
          headers: new Headers({
              'content-type': 'application/json',
              // 'Accept': 'application/json',
            }),
          // body: JSON.stringify({"url": "http://digitalnativestudios.com/textmeshpro/docs/rich-text/line-indent.png"})
          body: JSON.stringify(
              {
                  "tier": this.state.tier,
                  "id": this.convertHeroNameToId(this.state.favoriteHero),
              }
          ) 
        }
      );
    
    var rep = response.json()
    var passedRecommendedHeroesIds = await rep.then(function(value) {
        // console.log(value.res);
        return value.res;
      });
    console.log(passedRecommendedHeroesIds)
    // let passedRecommendedHeroesIds = [92,102,32,96,61,110,42,9,14,93,101,1,6,7,33,41];
    let passedRecommendedHeroesImages = this.convertIdsToFileNames(passedRecommendedHeroesIds);
    let images = FILE_NAMES.map( (name, index) => {
      const style = passedRecommendedHeroesImages.indexOf({name}.name) > -1 ? { border: '3px solid yellow' } : {border: '3px solid transparent'}
      const divstyle = {display: "inline-block"}
      const figcapstyle = {textAlign: 'center', color: "white"}
      let curtName = {name}.name.toString()
      let heroName = curtName.substring(0,curtName.length - 4)
      // console.log(curtName)
      return (
              <div style={divstyle}>
                <img key={index} 
                    style={style} 
                    title= {heroName} 
                    onClick={this.handleClickImage.bind(this, {name})} 
                    className="img-responsive" alt="" 
                    src={require(`./images/heros/${name}`)} />
                <figcaption style={figcapstyle}> {heroName}</figcaption>
              </div>
      )
    });
    // let passedRecommendedHeroesImages = convertIdToImage(passedRecommendedHeroesId);
    this.setState({images:images})
  }
  handleTierChange = (newTier) => {
    this.setState({tier: newTier});
  }
  handlefavoriteHeroChange = (newHero) => {
    this.setState({favoriteHero: newHero})
  }
  convertHeroNameToId = (heroName) => {
    var id = -1;
    let formattedInputName = ""
    for (let i = 0; i < heroName.length; i++) {
      let char = heroName.charAt(i)
      if ( char.toUpperCase() != char.toLowerCase()) {
        formattedInputName += char.toLowerCase()
      }
    }
    for (let curthero in hero) {
      var targetName = hero[curthero].localized_name;
      // console.log(hero[curthero].id)
      let formattedTargetName = ""
      for (let i = 0; i < targetName.length; i++) {   
        let char = targetName.charAt(i)
        if ( char.toUpperCase() != char.toLowerCase()) {
          formattedTargetName += char.toLowerCase()
        }
      }
      if (formattedTargetName === formattedInputName) {
        id = hero[curthero].id;
        break;
      }
    }
    console.log(id);
    return id;
  }
  handleDeleteHero = () => {
    let lastRound = this.state.round - 1;
    if (lastRound === 1 || lastRound === 4 || lastRound === 5 || lastRound === 8 || lastRound === 9) {
      let newMyTeamHeroes = this.state.myTeamHeroes.slice(0, -1);
      this.setState({
        myTeamHeroes : newMyTeamHeroes,
        round: lastRound
      })
    }
    if (lastRound === 2 || lastRound === 3 || lastRound === 6 || lastRound === 7 || lastRound === 10) {
      let newOpponentHeroes = this.state.opponentTeamHeroes.slice(0,-1);
      this.setState({
        opponentTeamHeroes : newOpponentHeroes,
        round: lastRound
      })
    }
  }
  

  render() {
    return (
      <div className="App" style={ backgroundStyle }>
          <div className="Predicter">
            <TeamPick 
              myTeamHeroes={this.state.myTeamHeroes} 
              opponentTeamHeroes={this.state.opponentTeamHeroes}
              handleDeleteHero={this.handleDeleteHero}
            ></TeamPick>
            <Result 
              resetTeamPick = {this.resetTeamPick}
              myTeamHeroes = {this.state.myTeamHeroes}
              opponentTeamHeroes = {this.state.opponentTeamHeroes}
              handleTierChange = {this.handleTierChange}
              handlefavoriteHeroChange = {this.handlefavoriteHeroChange}
              
            ></Result>
          </div>
          <div className="HeroPicker">
            <HeroPicker 
              handleClickImage = {this.handleClickImage}
              images = {this.state.images}
              ShowRecommendedHeroes = {this.ShowRecommendedHeroes}
            ></HeroPicker>
          </div>
      </div>
    );
  }
}

export default App;
