import {PureComponent} from "react";

class Header extends PureComponent {
    constructor(props) {
        super(props);
        this.state = {
            elementId: null
        }
    }

    static displayName = 'Header';

    render() {
        return (
            <div ref={header => this.header = header} id={this.props.elementId}>
                {this.props.data.image_type === 'Logo' &&
                    <div className="logo-view">
                        <div>
                            <img src={this.props.data.image} alt={this.props.data.heading}/>
                        </div>
                        <div className="heading">
                            <h1>{this.props.data.heading}</h1>
                            <span className="sub-heading">{this.props.data.sub_heading}</span>
                        </div>
                    </div>

                }
                {this.props.data.image_type === 'Banner' &&
                    <div className="banner-view">
                        <img src={this.props.data.image} alt={this.props.data.heading}/>
                        <div className="heading">
                            <h1>{this.props.data.heading}</h1>
                            <span className="sub-heading">{this.props.data.sub_heading}</span>
                        </div>
                    </div>
                }
            </div>
        );
    }

}

export default Header;