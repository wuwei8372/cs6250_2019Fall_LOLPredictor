import React, { Component } from 'react';
import '../css/HeroPicker.css';
class HeroPicker extends Component {
    // constructor(props) {
    //     super(props)
        
    //     this.state = {
    //         names : names,
    //   }
     
    // }
    handleClickImage = (item) => {
        //this.setState({species:e.target.value});
        this.props.handleClickImage(item);
        // console.log(item.name);
    };

    // onClick={this.onClick.bind(this, image.mediaId)}
  render() {
    return (
        <div className="HeroPicker">
            <footer className="row">
                <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6">
                    <h1>Please Select Heroes Below: </h1>
                    {/* <div>
                        <div className="square"/>
                        <h4> recommended heroes for you are circled in yellow color </h4>
                    </div>
                    <button onClick={this.props.ShowRecommendedHeroes}>
                        Give recommendations for heroes
                    </button> */}
                </div>
                <div className="col-xs-12 col-sm-6 col-md-6 col-lg-6">
                        { this.props.images }
                </div>
            </footer>
        </div>
    );
  }
}

export default HeroPicker;