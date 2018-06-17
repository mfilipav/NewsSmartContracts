contract NewsContract
{
   struct Journalist
   {
       string Name;
       string Address;
       bool headline;
       bool image;
       bool video;
       bool article;
       uint Amount;
   }
   
   struct NewsDetails
   {
       //details regarding Image, Video, Article would store the hash of the link to the actual data in the API
       string Headline;
       string Summary;
       string Article;
       string Image;
       string Video;
       string GUID;
       uint Price;
   }
   
   mapping (address => Journalist) journalists;
   address[] public JournalistsAcct;
   NewsDetails newsDetails;
   
   // Add new Journalist to the contract
   function AddJournalist (address addJourn) public{
       Journalist journalist = journalists[addJourn];
       journalist.Name ='Test';
       journalist.Address='Home Address';
       journalist.headline=false;
       journalist.image=false;
       journalist.video=false;
       journalist.article=false;
       journalist.Amount = 50;
       JournalistsAcct.push(addJourn);
   }
   
   function getJournalists() view public returns (address[]) {
       return JournalistsAcct;
   }
   
   function getJournalist(address ins) view public returns (string, string, bool, bool, bool, bool) {
       return (journalists[ins].Name, journalists[ins].Address, journalists[ins].headline, journalists[ins].image, journalists[ins].video, journalists[ins].article);
   }
   
   //Add NewsItem
   function AddNews(string _GUID, string _Headline, string _Summary, string _Article, string _Image, string _Video)
   public{
           //check to see if Journalist already exists
           
           //if not exists Add Journalist
           AddJournalist(msg.sender);
           
           if (bytes(_Headline).length != 0)
               journalists[msg.sender].headline=true;
           if (bytes(_Article).length != 0)
               journalists[msg.sender].article=true;
           if (bytes(_Image).length != 0)
               journalists[msg.sender].image=true;
           if (bytes(_Video).length != 0)
               journalists[msg.sender].video=true;
           
           newsDetails.GUID = _GUID;
           if (bytes(_Headline).length != 0)
               newsDetails.Headline = _Headline;
           if (bytes(_Summary).length != 0)
               newsDetails.Summary = _Summary;
           if (bytes(_Article).length != 0)
               newsDetails.Article = _Article;
           if (bytes(_Image).length != 0)    
               newsDetails.Image = _Image;
           if (bytes(_Video).length != 0)    
               newsDetails.Video = _Video;
               
           // Assume fixed Price per NewsItem. This can be enhance to be based on how much a Journalist wants
           
           newsDetails.Price = 1;
       }
       
    function getPricePerRequest(bool _article, bool _image, bool _video) view public returns (uint){
       //Determine the price of the News based on the content requested
       
       uint cost = newsDetails.Price * 1;
       // For each content we increase the price of the request
       if (_article == true) cost += 1;
       if (_image == true) cost += 1;
       if (_video == true) cost += 1;
       return cost;
   }
   //BuyNews
   function BuyNews(bool _article, bool _image, bool _video)
   public payable returns(string, string, string, string){
       //Assume they always get the Headline
       string Headline = newsDetails.Headline;
       string Article;
       string Image;
       string Video;
       
       // Check the price it value returned matches the sender
       uint _price = getPricePerRequest(_article, _image, _video);
       require(msg.value == _price ); 
       //uint cost = price * ();
       
       address[] JourAddress = JournalistsAcct;
       
       for (uint i=0; i<JourAddress.length; i++) {
            //Logic to weight the payment to the Journalist based on his content
           //Update balance of each Journalist
           journalists[JourAddress[i]].Amount += newsDetails.Price;
           JourAddress[i].transfer(msg.value);
           
       }
       
       //Return content based on decision
       if (_article == true) Article = newsDetails.Article;
       if (_image == true) Image = newsDetails.Image;
       if (_video == true) Video = newsDetails.Video;
       
       return (Headline, Article, Image, Video);
   }
}