const isEmpty =  require('./isEmpty');
const Validator = require('validator');
var exports = module.exports={};

//this function works but feel free to use your code 
//however make sure your code takes a string and not an array as my other three do.
const validateSearchSmiles=(data)=>{
    let errors = {};
    /*let notSmile = data.filter(smile=>{
        if(!Validator.matches(smile,/^([^J][A-Za-z0-9@+\-[]()=#$]+)$/)){
        //if(!Validator.matches(smile,/^([^J][A-Za-z0-9@+\-\[\]\(\)\\=#$]+)$/)){
            return smile;
        }
        return smile;
    });*/
    let notSmile;
    if(!Validator.matches(data,/^([^J][A-Za-z0-9@+\-[]()=#$]+)$/)){
        //if(!Validator.matches(smile,/^([^J][A-Za-z0-9@+\-\[\]\(\)\\=#$]+)$/)){
            notSmile=data;
        }
  
    if (!isEmpty(notSmile)){
        console.log(notSmile)
        errors.notSmile=[...notSmile];
    }
    return {
        errors,
        isValid:isEmpty(errors)}
}
//validate keyword searches
const validateKeyword =(inputedString)=>{
    let validatedInput=false; 
    let error_message='';
    console.log("starting keyword validation...");
    //convert to lower case
    inputedString=inputedString.toLowerCase();
    //designing regex to contain charactes 0-9 a-z - ( ) [ ] spaces 
    let myRegex =new RegExp("^[a-z0-9\\-\\[\\]\\(\\)]+$");
    //let myRegex2=new RegExp("\\'|;|,|?|!|@|#|$|%|^|&|*|_|+|=|{|}|\\||:|\"|/|>|<|.|~|`/g");
    
    if (myRegex.test(inputedString)  && inputedString.length<758){
      validatedInput=true;
    }
    else if (myRegex.test(inputedString)===true && inputedString.length>757){
      validatedInput=false;
      error_message=inputedString+": compound name must be less than 757 characters.";
      console.log(error_message);
    }
    else if (myRegex.test(inputedString)=== false && inputedString.length<758){
        validatedInput=false;
        error_message=inputedString+": invalid compound name. keyword search can only contain alpha-numeric characters, as well as (,),[,],-.";
        console.log(error_message);
      }
    else {
        error_message="invalid entry";
        console.log(error_message);
    }
    console.log(validatedInput);

    return error_message, validatedInput;
  }
//validate InChiKeys strings 
const validateInchikey=(inputedString)=>{
    let inchikey_rules=["International Chemical Identifier KEY validation rules.  InChIKey consists of several distinct components:",
    "- 14 characters resulting from a hash of the connectivity information of the InChI,encodes molecular skeleton (connectivity). ",
    "- followed by a hyphen,",
    "- followed by 8 characters resulting from a hash of the remaining layers of the InChI, ",
    "- Encodes proton positions (tautomers), stereochemistry, isotopomers, reconnected layer  ",
    "- followed by a single character indicating the kind of InChIKey, ",
    "- followed by a single character indicating the version of InChI used, ",
    "- another hyphen, ",
    "- followed by single character indicating protonation.(Source: Wikipedia). ",
    "  AAAAAAAAAAAAAA-BBBBBBBBCD-E "].join ("\n");
    
    let myRegex = new RegExp('[A-Z\\-]+');
    let validatedValue=false;
    let error_message='';
    var i=inputedString.toUpperCase().trim(" ");
   
    //if all conditions are met
    if (i.length===27 && myRegex.test([i])===true && i[14]==='-'&&i[25]==='-'){
        validatedValue=true;
        }
    //incorrect length of string 
    else if (i.length!==27){
        validatedValue=false;
        error_message="Error! Invalid inchikey string length: "+i+".";
        console.log(error_message);
        }
    // incorrect length of fragments 
    else if(!myRegex.test(i) || i[14]!=='-' || i[24]!=='-'){
        validatedValue=false
        error_message="Error! The lengths of the inchikey fragments is invalid.: "+i+".";
        console.log(error_message);
        }
    else {
            error_message="Error! Invalid inchikey string: "+i;
            console.log(error_message);
            validatedValue=false;
        }
        let errors=error_message.concat("\n",inchikey_rules);
        //console.log(errors, validatedValue);
    return {errors, validatedValue};
}
//validate CAS Numbers
const validateCAS=(inputedString)=>{
  let cas_rules=['A CAS Registry Number includes up to 10 digits which are separated in 3 hyphens.',
  'The first part of the number, starting from the left, has 2 to 7 digits.',
  'The second part has 2 digits.',
  'The final part consists of a single check digit.'].join('\n');
  
  let validatedValue=false;
  let myRegex=new RegExp('^[0-9]{2,7}[\\-][0-9]{2}[\\-][0-9]$');
  let error_message="";
  
  //if the string has the exact requirements of CAS
  if (myRegex.test(inputedString)){
      validatedValue=true; 
  }
  else {
        //remove any symbols including hyphens
        myRegex1="'|;|,|?|!|-|@|#|$|%|^|&|*|_|+|=|{|}|[||\\|:|\"|/|>|<|.|~|`/g";
        inputedString=inputedString.trim().replace(myRegex1,"");
        myRegex=new RegExp('^[0-9A-Z]$');
        
        //if the string only contains numbers, check its length
        if (inputedString.length>10 ||inputedString.length<5 ){
        validatedValue=false;
        error_message="CAS Number "+inputedString+" is invalid. The number of digits must be between 5 and 10.";
        console.log(error_message);
        }  
        
        //if the string contains alphanumeric characters
        else if (myRegex.test(inputedString)===false){
          validatedValue=false;
          error_message="Invalid CAS Number "+inputedString+": CAS numbers should consist of digits only and hyphens. Review the validations rules.";
          console.log(error_message);
          }
        //myRegex=new RegExp('^[0-9]{5,10}$');
        //correct number of digits
       else {     
            validatedValue=false;
            error_message='Invalid CAS Number entry '+inputedString+". Please review the validation rules for CAS numbers.";
            console.log(error_message);
      }
  }
  console.log(error_message+"\n"+validatedValue)
  return {error_message,validatedValue};
}
exports.validateSearch = function validateSearch(selectedIdentifier, chems){
    let chemsValid;
    let chemsValidCounter=0;
    for (let i=0; i<chems.length;i++){
        if(selectedIdentifier==='keyword'){
            chemsValid=validateKeyword(chems[i]);
            return chemsValid;
        }
        else if(selectedIdentifier==='CAS'){
            chemsValid=validateCAS(chems[i]);
            return chemsValid;
        }
        else if(selectedIdentifier==='inchikey'){
            chemsValid=validateInchikey(chems[i]);
            return chemsValid;
        }
        else {
        //selectedIdentifier is a Canonical SMILES
        chemsValid=validateSearchSmiles(chems[i]);
        return chemsValid;
        }
        object.keys(chemsValid)[1]===false?chemsValidCounter+=1 : chemsValidCounter+=0;
    }
    chemsValidCounter>0?object.keys(chemsValid)[1]=true:object.keys(chemsValid)[1]=false;
    console.log(chemsValid);
    return chemsValid;
} 