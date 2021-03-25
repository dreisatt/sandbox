import { Friend, Friends } from "../../model/index";
import { API_BASE_URL } from "../config/api.config";

export class FriendService {
  getFriends(): Promise<Friends> {
    return fetch(`${API_BASE_URL}/friends`)
      .then(response => response.json())
      .then((data: Friends) => data);
  }
}