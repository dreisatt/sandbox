import * as React from "react";
import { FriendComponent } from "coding_sandbox/react_app/frontend/friend/friend";
import { FriendService } from "coding_sandbox/react_app/frontend/friend/friend-service";
import { Friend, Friends } from "../model/index";

export class FriendsList extends React.Component<{}, Friends> {
  friendService = new FriendService();

  constructor(props) {
    super(props);
    const friends: Friends = new Friends;
    this.state = friends;
  }

  render() {
    const friends = this.state.getFriendsList().map((friend: Friend) => {
      return (
        <FriendComponent id={friend.getId()} name={friend.getName()} />
      );
    });
    return (
      <div>
        <h1>List of Friends!</h1>
        {friends}
      </div>
    );
  }

  componentDidMount() {
    this.friendService.getFriends().then(result => this.setState({...result,}));
  }
}