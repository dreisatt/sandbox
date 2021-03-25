import * as React from "react";

export interface PropFriend
{
  id: number,
  name: string,
};

export class FriendComponent extends React.Component<PropFriend, {}> {
  render() {
    return (
      <div>
        {this.props.id} {this.props.name}
      </div>
    );
  }
}