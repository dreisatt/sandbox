import * as React from "react";
import * as ReactDOM from "react-dom";
import { FriendsList } from "./app";
import {Friend, Friends} from "../model/index"

ReactDOM.render(<FriendsList {...new Friends}/>, document.getElementById("root"));