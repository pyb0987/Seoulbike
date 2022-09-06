import axios from 'axios';
import _ from 'lodash';
import {authRequest } from 'src/login/auth'

const USERSPOTS = 'userspots'
const UsetLikeSpotsLIST = 'userspotslist'


const getLikeSpots = ()=>{
  let data = window.localStorage.getItem(USERSPOTS)
  let parsedData = JSON.parse(data)
  if(!parsedData){
    parsedData = []
  }
  return parsedData
}
const getLikeSpotsList = ()=>{
  let data = window.localStorage.getItem(UsetLikeSpotsLIST)
  let parsedData = JSON.parse(data)
  if(!parsedData){
    parsedData = []
  }
  return parsedData
}
const setLikeSpots = (data)=>{
  let datalist = data.map(x=>x.idnumber)
  let stringfiedList = JSON.stringify(datalist)
  let stringfiedData = JSON.stringify(data)
  window.localStorage.setItem(USERSPOTS, stringfiedData)
  window.localStorage.setItem(UsetLikeSpotsLIST, stringfiedList)
}
const updateLikeSpots = (data)=>{
  let target = getLikeSpots()
  let mergedTarget
  if (!!target){
    mergedTarget = _.uniqWith(_.concat(target, data), function(x, y){
      return x.idnumber === y.idnumber
    });
  }else{
    mergedTarget = data
  }
  setLikeSpots(mergedTarget)
}
const deleteSpots = ()=>{
  window.localStorage.removeItem(USERSPOTS);
  window.localStorage.removeItem(UsetLikeSpotsLIST);
}

const likeAspot = (data)=>{ //like, dislike
  let target = getLikeSpots();
  let likedTarget = _.xorWith(target, [data], function(x, y){
    return x.idnumber === y.idnumber
  });
  setLikeSpots(likedTarget)
}


const LoginSpotGet = async (user_id)=>{  //로그인시 실행하여 스팟을 불러들임
  try{
    console.log('resbefore')
    let res = await authRequest.get(`http://localhost:8000/api/seoulbike/user/${user_id}/spots`)
    console.log('res',res)
    updateLikeSpots(res.data)
  }catch(err){
    console.log(err)
  }
}

const LogoutSpotSet = async (user_id)=>{  //로그아웃시 실행하여 스팟을 db에 저장함
  let spots = getLikeSpotsList()
  try{
    let res = await authRequest.put(`http://localhost:8000/api/seoulbike/user/${user_id}/spots/`,{user_spots : spots})
    console.log(res)
  }catch(err){
    console.log(err)
  }
}


export {
  LoginSpotGet, LogoutSpotSet, getLikeSpots, getLikeSpotsList, updateLikeSpots, likeAspot
};