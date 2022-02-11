void runAnalysis(){

  // gROOT->Reset();
//remove the stat from upper right corner
  gStyle->SetOptStat(0);
  //remove the title
  gStyle->SetOptTitle(0);
  //define fonts sizes
  gStyle->SetTextSize(0.06);
  gStyle->SetLabelSize(0.06,"x");
  gStyle->SetLabelSize(0.06,"y");
  gStyle->SetLabelSize(0.06,"z");
  gStyle->SetTitleSize(0.06,"x");
  gStyle->SetTitleSize(0.05,"y");
  gStyle->SetTitleSize(0.06,"z");
  //define number of divisions on any axis, here is done only for "Y"
  gStyle->SetNdivisions(505,"y");
  gStyle->SetLineWidth(3);

  
 
  TFile* inputFile=TFile::Open("output/test.root");
 
   if (!inputFile)
     {
       Error("","file not found");
       exit(1);
     }

   //////////////////////////
   ////   Hits Tree    //////
   /////////////////////////
   TTree* hitTree = (TTree*)inputFile->Get("Hits");
   //  cout<< hitTree->GetEntries()<<endl;
  
   
   Int_t    PDGEncoding_hit;     	      	      	//!< PDG encoding of the particle
   Int_t    trackID_hit; 	      	      	      	//!< Track ID
   Int_t    parentID_hit;	      	      	      	//!< Parent ID
   Double_t time_hit;    	      	      	      	//!< Time of the hit (in seconds)
   Double_t trackLocalTime_hit;    	      	      	//!< Time of the current track (in seconds)
   Float_t  edep_hit;    	      	      	      	//!< Deposited energy (in MeVs)
   Float_t  stepLength_hit;      	      	      	//!< Step length (in millimeters)
   Float_t  trackLength_hit;      	      	      	//!< Track length (in millimeters)
   Float_t  posX_hit,posY_hit,posZ_hit;  	      	      	//!< Global hit position (in millimeters)
   Float_t  momDirX_hit,momDirY_hit,momDirZ_hit;                //!< Global hit momentum
   Float_t  localPosX_hit, localPosY_hit, localPosZ_hit; 	//!< Local hit position (in millimeters)
   Int_t    gantryID_hit, blockID_hit, crystalID_hit;         	//!< 6-position output ID
   Int_t    photonID_hit;	      	      	      	//!< Photon ID
   Int_t    nPhantomCompton_hit; 	      	      	//!< Number of Compton interactions in the phantom
   Int_t    nCrystalCompton_hit; 	      	      	//!< Number of Compton interactions in the crystam
   Int_t    nPhantomRayleigh_hit; 	      	      	//!< Number of Rayleigh interactions in the phantom
   Int_t    nCrystalRayleigh_hit; 	      	      	//!< Number of Rayleigh interactions in the crystam
   Int_t    primaryID_hit;       	      	      	//!< Primary ID
   Float_t  sourcePosX_hit,sourcePosY_hit,sourcePosZ_hit;	//!< Global decay position (in millimeters)
   Int_t    sourceID_hit;	      	      	      	//!< Source ID
   Int_t    eventID_hit; 	      	      	      	//!< Event ID
   Int_t    runID_hit;   	      	      	      	//!< Run ID
   Float_t  axialPos_hit;	      	      	      	//!< Scanner axial position (in millimeters)
   Float_t  rotationAngle_hit;           	      	//!< Rotation angle (in degrees)
   Char_t   processName_hit[40]; 	      	      	//!< Name of the process that generated the hit
   Char_t   comptonVolumeName_hit[40];   	      	//!< Name of the last phantom-volume generating a Compton
   Char_t   RayleighVolumeName_hit[40];   	      	//!< Name of the last phantom-volume generating a Rayleigh
   Int_t    volumeID_hit[10];                	//!< Volume ID

   Int_t sourceType_hit; //Type of gamma source (check ExtendedVSource)
   Int_t decayType_hit; //Type of positronium decay (check ExtendedVSource)
   Int_t gammaType_hit; //Gamma type - single, annhilation, prompt (check ExtendedVSo
    


   hitTree->SetBranchAddress("PDGEncoding",&PDGEncoding_hit);
   hitTree->SetBranchAddress("trackID",&trackID_hit);
   hitTree->SetBranchAddress("parentID",&parentID_hit);
   hitTree->SetBranchAddress("time",&time_hit);
   hitTree->SetBranchAddress("edep",&edep_hit);
   hitTree->SetBranchAddress("stepLength",&stepLength_hit);
   hitTree->SetBranchAddress("posX",&posX_hit);
   hitTree->SetBranchAddress("posY",&posY_hit);
   hitTree->SetBranchAddress("posZ",&posZ_hit);
   hitTree->SetBranchAddress("localPosX",&localPosX_hit);
   hitTree->SetBranchAddress("localPosY",&localPosY_hit);
   hitTree->SetBranchAddress("localPosZ",&localPosZ_hit);
   hitTree->SetBranchAddress("momDirX",&momDirX_hit);
   hitTree->SetBranchAddress("momDirY",&momDirY_hit);
   hitTree->SetBranchAddress("momDirZ",&momDirZ_hit);
   hitTree->SetBranchAddress("gantryID",&gantryID_hit);
   hitTree->SetBranchAddress("blockID",&blockID_hit);
   hitTree->SetBranchAddress("crystalID",&crystalID_hit);
   hitTree->SetBranchAddress("photonID",&photonID_hit);
   hitTree->SetBranchAddress("nPhantomCompton",&nPhantomCompton_hit);
   hitTree->SetBranchAddress("nCrystalCompton",&nCrystalCompton_hit);
   hitTree->SetBranchAddress("nPhantomRayleigh",&nPhantomRayleigh_hit);
   hitTree->SetBranchAddress("nCrystalRayleigh",&nCrystalRayleigh_hit);
   hitTree->SetBranchAddress("primaryID",&primaryID_hit);
   hitTree->SetBranchAddress("sourcePosX",&sourcePosX_hit);
   hitTree->SetBranchAddress("sourcePosY",&sourcePosY_hit);
   hitTree->SetBranchAddress("sourcePosZ",&sourcePosZ_hit);
   hitTree->SetBranchAddress("sourceID",&sourceID_hit);
   hitTree->SetBranchAddress("eventID",&eventID_hit);
   hitTree->SetBranchAddress("runID",&runID_hit);
   hitTree->SetBranchAddress("axialPos",&axialPos_hit);
   hitTree->SetBranchAddress("rotationAngle",&rotationAngle_hit);
   hitTree->SetBranchAddress("processName",&processName_hit);
   hitTree->SetBranchAddress("comptVolName",&comptonVolumeName_hit);
   hitTree->SetBranchAddress("RayleighVolName",&RayleighVolumeName_hit);
   hitTree->SetBranchAddress("volumeID",volumeID_hit);
   hitTree->SetBranchAddress("sourceType",&sourceType_hit);
   hitTree->SetBranchAddress("decayType",&decayType_hit);
   hitTree->SetBranchAddress("gammaType",&gammaType_hit);


   ////////////////////////////////////
   //// Singles Tree 
   //////////////////////////////////

   TTree* singleTree = (TTree*)inputFile->Get("Singles");
   //  cout<< singleTree->GetEntries()<<endl;
   Int_t    runID_single;
   Int_t    eventID_single;
   Int_t    sourceID_single;
   Float_t  sourcePosX_single;
   Float_t  sourcePosY_single;
   Float_t  sourcePosZ_single;
   Double_t time_single;
   Float_t  energy_single;
   Float_t  globalPosX_single;
   Float_t  globalPosY_single;
   Float_t  globalPosZ_single;
   Int_t    gantryID_single, blockID_single, crystalID_single;
   Int_t    comptonPhantom_single; 
   Int_t    comptonCrystal_single;    
   Int_t    RayleighPhantom_single; 
   Int_t    RayleighCrystal_single;    
   Float_t  axialPos_single;
   Float_t  rotationAngle_single;    
   Char_t   comptVolName_single[40];
   Char_t   RayleighVolName_single[40];

   singleTree->SetBranchAddress("runID",&runID_single);
   singleTree->SetBranchAddress("eventID",&eventID_single);
   singleTree->SetBranchAddress("sourceID",&sourceID_single);
   singleTree->SetBranchAddress("sourcePosX",&sourcePosX_single);
   singleTree->SetBranchAddress("sourcePosY",&sourcePosY_single);
   singleTree->SetBranchAddress("sourcePosZ",&sourcePosZ_single);
   singleTree->SetBranchAddress("time",&time_single);
   singleTree->SetBranchAddress("energy",&energy_single);
   singleTree->SetBranchAddress("globalPosX",&globalPosX_single);
   singleTree->SetBranchAddress("globalPosY",&globalPosY_single);
   singleTree->SetBranchAddress("globalPosZ",&globalPosZ_single);
   singleTree->SetBranchAddress("gantryID",&gantryID_single);
   singleTree->SetBranchAddress("blockID",&blockID_single);
   singleTree->SetBranchAddress("crystalID",&crystalID_single);
   singleTree->SetBranchAddress("comptonPhantom",&comptonPhantom_single);
   singleTree->SetBranchAddress("comptonCrystal",&comptonCrystal_single);
   singleTree->SetBranchAddress("RayleighPhantom",&RayleighPhantom_single);
   singleTree->SetBranchAddress("RayleighCrystal",&RayleighCrystal_single);
   singleTree->SetBranchAddress("axialPos",&axialPos_single);
   singleTree->SetBranchAddress("rotationAngle",&rotationAngle_single);
   singleTree->SetBranchAddress("comptVolName",&comptVolName_single);
   singleTree->SetBranchAddress("RayleighVolName",&RayleighVolName_single); 


   //Histo for comparison
   TH1F *h_hits_totEdep = new TH1F("h_hits_totEdep","h_hits_totEdep",100,0.,0.6);
   TH1F *h_singles_energy = new TH1F("h_singles_energy","h_singles_energy",100,0.,0.6);

   
   TH1D *h_hits_minTime = new TH1D("h_hits_minTime","h_hits_minTime",100,0.,0.012);
   TH1D *h_singles_time = new TH1D("h_singles_time","h_singles_time",100,0.,0.012);


   TH1D *h_hits_X = new TH1D("h_hits_X","h_hits_X",100,-200,200);
   TH1D *h_singles_X = new TH1D("h_singles_X","h_singles_X",100,-200,200);


   TH1D *h_hits_Y = new TH1D("h_hits_Y","h_hits_Y",100,-200,200);
   TH1D *h_singles_Y = new TH1D("h_singles_Y","h_singles_Y",100,-200,200);


   TH1D *h_hits_Z = new TH1D("h_hits_Z","h_hits_Z",100,-5,5);
   TH1D *h_singles_Z = new TH1D("h_singles_Z","h_singles_Z",100,-5,5);
   //Coincidences->SetBranchAddress("RayleighCrystal2",&RayleighCrystal2);




   ////////////////////// hits processing
   int tempID=-1;
   int currentBlockID=-1;
   int currentEventID=-1;
   int prevIterEventID=-1;
   int prevIterBlockID=-1;

   int nextIterEventID=-1;
   int nextIterBlockID=-1;


   float currentEdep;
   double currentTime;
   // float maxEdep=-1;
   //float totEdep=0;
   //double minTime=999;

   float currentX, currentY, currentZ;
   // float winnerX, winnerY, winnerZ;

   float testX[35];
   float testY[35];
   float testZ[35];
   int j=0;

   vector<int> v_blockID;
   vector<float> v_currentEdep;
   vector<double> v_currentTime;
   vector<float> v_currentX;
   vector<float> v_currentY;
   vector<float> v_currentZ; 
     
   for(Int_t i=0;i<hitTree->GetEntries();i++)
   // for(Int_t i=0;i<5;i++)
     {
       hitTree->GetEntry(i);
       currentEventID=eventID_hit;
       currentBlockID=blockID_hit;


       currentEdep=edep_hit;
       currentTime=time_hit;

       currentX=posX_hit;
       currentY=posY_hit;
       currentZ=posZ_hit;

       if (i== hitTree->GetEntries()-1) // last iteration
	 nextIterEventID=-1;
       else //all other iterations
	 {
	   hitTree->GetEntry(i+1);
	   nextIterEventID=eventID_hit;
	 }
       
       
       // cout<<"Entrie "<< i<<endl;
       //cout<< currentEventID<<" "<<currentBlockID<<" "<<currentEdep<<" "<<currentTime*100000 <<endl;
       //  printf("%d %d %f %f %f %f %.12f \n",  currentEventID, currentBlockID, currentEdep, currentX, currentY, currentZ, currentTime );//prevIterEventID,prevIterBlockID,currentEventID, currentBlockID,  nextIterEventID, nextIterBlockID );
       // cout<< currentEventID<<" "<<currentBlockID<<" "<<currentEdep<<" "<<currentTime*100000 <<endl;
       // printf("%d %d %f %f \n", currentEventID, currentBlockID, currentEdep, currentX);


	/////////////
	  if (currentEdep != 0)//   continue; //if not we loose events where last hit has edep=0
	    {
	      v_blockID.push_back(currentBlockID);
	      v_currentEdep.push_back(currentEdep);
	      v_currentTime.push_back(currentTime);
	      v_currentX.push_back(currentX);
	      v_currentY.push_back(currentY);
	      v_currentZ.push_back(currentZ);
	    }
	 
	 
	 if (currentEventID != nextIterEventID ) //if next event is new: analyse and clear all vectors
	   {
	      
	     
	     //How many unique blocks?
	     vector<int> v_uniqueblockID;
	     //cout<<"block IDs size " << v_blockID.size()<<endl;
	     for (int j=0; j<v_blockID.size();j++)
	       {
		 if(std::find(v_uniqueblockID.begin(),  v_uniqueblockID.end(), v_blockID[j]) == v_uniqueblockID.end())
		   {
		     v_uniqueblockID.push_back(v_blockID[j]);
		   }
	       }
	     
	     //cout<<"N unique block IDs " << v_uniqueblockID.size()<<endl;

		      
	     float maxEdep[v_uniqueblockID.size()];
	     float totEdep[v_uniqueblockID.size()];
	     double minTime[v_uniqueblockID.size()];
	     float winnerX[v_uniqueblockID.size()];
	     float winnerY[v_uniqueblockID.size()];
	     float winnerZ[v_uniqueblockID.size()];
	     
	     for (int k=0; k<v_uniqueblockID.size();k++)
	       {
		 maxEdep[k]=-1;
		 totEdep[k]=0;
		 minTime[k]=999;
	
		 
	       }	 
		 
	     for (int j=0; j<v_blockID.size();j++)
	       {
		 
		 
		 for (int k=0; k<v_uniqueblockID.size();k++)
		   {
		     
		     
		     
		     if (v_blockID[j]==v_uniqueblockID[k])
		       {
			 //cout<< v_blockID[j]<<endl;
			 
			 //find max energy
			 if (v_currentEdep[j]>=maxEdep[k])
			   {
			     maxEdep[k]=v_currentEdep[j];
			     winnerX[k]=v_currentX[j];
			     winnerY[k]=v_currentY[j];
			     winnerZ[k]=v_currentZ[j]; 
			   }
			 
			 //find min time
			 if (v_currentTime[j]<minTime[k])
			   {
			     minTime[k]=v_currentTime[j];
			   }
			 
			 
			 //summ of dep energy 
			 totEdep[k] += v_currentEdep[j]; 	   
		       }
		     
		     
		   }
		 
	       }
		 
	     for (int k=0; k<v_uniqueblockID.size();k++)
	       {
		 h_hits_totEdep->Fill(totEdep[k]);
		 h_hits_minTime->Fill(minTime[k]);
		 h_hits_X->Fill(winnerX[k]);
		 h_hits_Y->Fill(winnerY[k]);
		 h_hits_Z->Fill(winnerZ[k]);
		 if (totEdep[k] >0.512)
		  printf("something is wrong");
		 
		 //  printf("! %d %f %f %f %f %.12f\n", v_uniqueblockID[k], totEdep[k], winnerX[k], winnerY[k],winnerZ[k],  minTime[k]);
		 
	       }
	     		
	     v_blockID.clear();
	     v_currentEdep.clear();
	     v_currentTime.clear(); 
	     v_currentX.clear();
	     v_currentY.clear();
	     v_currentZ.clear();
	     
		
	   }
	 
     }
   ///////////////////// SINGLES processing    
   	 
   for(Int_t i=0;i<singleTree->GetEntries();i++)
     //for(Int_t i=0;i<30;i++)
     {
       
       singleTree->GetEntry(i);
       h_singles_energy->Fill(energy_single);
       h_singles_time->Fill(time_single);
       
       
       
       h_singles_X->Fill(globalPosX_single);
       h_singles_Y->Fill(globalPosY_single);  			       
       h_singles_Z->Fill(globalPosZ_single);
       //printf("%d %f %f %f %f %.12f\n",blockID_single, energy_single,globalPosX_single, globalPosY_single,globalPosZ_single,  time_single);
       //  printf("%d %d\n",eventID_single,blockID_single);//, energy_single,globalPosX_single, globalPosY_single,globalPosZ_single,  time_single);
       // printf("%d %d %f %f %f %f %.12f\n",eventID_single, blockID_single, energy_single,globalPosX_single, globalPosY_single,globalPosZ_single,  time_single);
       //  printf("%d %d %f %f %f %f %.12f\n",eventID_single,blockID_single, energy_single,globalPosX_single, globalPosY_single,globalPosZ_single,  time_single);
       /* if( globalPosY_single != testY[i])
	 {
	   printf("%f %f %f %f %f \n", energy_single,globalPosX_single, globalPosY_single , globalPosZ_single);
	   printf("%f %f %f %f \n", energy_single,testX[i], testY[i], testZ[i]);
	 }
       */
     }


   /// N entries test
   if (h_hits_totEdep->GetEntries() == singleTree->GetEntries())
     cout<< "Entries test is OK: "<< h_hits_totEdep->GetEntries() << " vs. " <<  singleTree->GetEntries() <<endl;
   else cout << "\033[1;31m!!! Entries test failed !!! \033[0m"<< h_hits_totEdep->GetEntries() << " vs. " <<  singleTree->GetEntries() <<endl;



 
   TCanvas *cc =new TCanvas("cc","cc",1000,500*2) ;
   cc->Divide(2,3);

   cc->cd(1);

   
   h_hits_totEdep->SetLineWidth(1);
   h_hits_totEdep->SetLineColor(1);
   h_hits_totEdep->GetXaxis()->SetTitle("Energy, MeV");
   h_hits_totEdep->GetYaxis()->SetTitleOffset(1.0); 
   h_hits_totEdep->GetYaxis()->SetTitle("Arbitrary units");
  
   h_hits_totEdep->Draw();

   h_singles_energy->SetMarkerStyle(2);
   h_singles_energy->SetMarkerColor(2);
   h_singles_energy->SetLineColor(2);
   //h_singles_energy->SetMarkerSize(3);
   h_singles_energy->Draw("esame");


   float sum_diff_energy = 0;
   for (int i=0; i<h_hits_totEdep->GetNbinsX();i++)
     {
       float mean= (h_singles_energy->GetBinContent(i) + h_hits_totEdep->GetBinContent(i))/2;
       if(mean==0) continue;       
       float diff =  fabs(h_singles_energy->GetBinContent(i) - h_hits_totEdep->GetBinContent(i))/mean ;
       sum_diff_energy += diff;
     }

   float test_energy = sum_diff_energy/h_hits_totEdep->GetNbinsX()*100;

   TString* str_energy = new TString(Form("rel. diff = %.2f %c",test_energy, '%'));
   TLatex *myTex_energy = new TLatex(0.25, 0.8, *str_energy);
   myTex_energy->SetNDC();
   myTex_energy->SetTextSize(0.05);
   myTex_energy->Draw();
   //cc->addObject( myTex );
   
    if (test_energy)
      cout << "\033[1;31m!!! Total deposited energy test faied !!! \033[0m"<< test_energy <<endl; 
   
   

   TLegend* leg = new TLegend(0.2126999,0.5370618,0.564629,0.665473,NULL,"brNDC");
   leg->SetBorderSize(0);
   leg->SetTextFont(62);
   leg->SetTextSize(0.05);
   leg->SetFillColor(0);
   leg->SetFillStyle(1001);
   leg->AddEntry(h_hits_totEdep, "Offline Digi", "l");
   leg->AddEntry(h_singles_energy, "Gate Digi", "p");
   leg->Draw();


   cc->cd(2);

   
   h_hits_minTime->SetLineWidth(1);
   h_hits_minTime->SetLineColor(1);
   h_hits_minTime->GetXaxis()->SetTitle("Min time, s");
   h_hits_minTime->GetYaxis()->SetTitleOffset(1.0); 
   h_hits_minTime->GetYaxis()->SetTitle("Arbitrary units");
  
   h_hits_minTime->Draw();

   h_singles_time->SetMarkerStyle(2);
   h_singles_time->SetMarkerColor(2);
   h_singles_time->SetLineColor(2);
   //h_singles_energy->SetMarkerSize(3);
   h_singles_time->Draw("same");


   float sum_diff_time = 0;
   for (int i=0; i<h_hits_minTime->GetNbinsX();i++)
     {
       float mean= (h_singles_time->GetBinContent(i) + h_hits_minTime->GetBinContent(i))/2;
       if(mean==0) continue;       
       float diff =  fabs(h_singles_time->GetBinContent(i) - h_hits_minTime->GetBinContent(i))/mean ;
       sum_diff_time += diff;
     }

   float test_time = sum_diff_time/h_hits_minTime->GetNbinsX()*100;

   TString* str_time = new TString(Form("rel. diff = %.2f %c",test_time,'%'));
   TLatex *myTex_time = new TLatex(0.25, 0.2, *str_time);
   myTex_time->SetNDC();
   myTex_time->SetTextSize(0.05);
   myTex_time->Draw();
   
   if (test_time)
      cout << "\033[1;31m!!! Min time test faied !!! \033[0m"<< test_time <<endl; 
   
   cc->cd(3);

   h_hits_X->SetLineWidth(1);
   h_hits_X->SetLineColor(1);
   h_hits_X->GetXaxis()->SetTitle("global X, cm");
   h_hits_X->GetYaxis()->SetTitleOffset(1.0); 
   h_hits_X->GetYaxis()->SetTitle("Arbitrary units");
  
   h_hits_X->Draw();

   h_singles_X->SetMarkerStyle(2);
   h_singles_X->SetMarkerColor(2);
   h_singles_X->SetLineColor(2);
   //h_singles_energy->SetMarkerSize(3);
   h_singles_X->Draw("same");

   float sum_diff_X = 0;
   for (int i=0; i<h_hits_X->GetNbinsX();i++)
     {
       float mean= (h_singles_X->GetBinContent(i) + h_hits_X->GetBinContent(i))/2;
       if(mean==0) continue;       
       float diff =  fabs(h_singles_X->GetBinContent(i) - h_hits_X->GetBinContent(i))/mean ;
       sum_diff_X += diff;

       // if(h_singles_X->GetBinContent(i)!=h_hits_X->GetBinContent(i))
       // cout<<"wrond bin"<<h_hits_X->GetBinCenter(i) <<" "<<h_singles_X->GetBinContent(i)<<endl;
       
     }

   float conclusion_X = sum_diff_X/h_hits_X->GetNbinsX()*100;

   TString* str_X = new TString(Form("rel. diff = %.2f %c",conclusion_X,'%'));
   TLatex *myTex_X = new TLatex(0.25, 0.2, *str_X);
   myTex_X->SetNDC();
   myTex_X->SetTextSize(0.05);
   myTex_X->Draw();


   cc->cd(4);

   h_hits_Y->SetLineWidth(1);
   h_hits_Y->SetLineColor(1);
   h_hits_Y->GetXaxis()->SetTitle("global Y, cm");
   h_hits_Y->GetYaxis()->SetTitleOffset(1.0); 
   h_hits_Y->GetYaxis()->SetTitle("Arbitrary units");
  
   h_hits_Y->Draw();

   h_singles_Y->SetMarkerStyle(2);
   h_singles_Y->SetMarkerColor(2);
   h_singles_Y->SetLineColor(2);
   //h_singles_energy->SetMarkerSize(3);
   h_singles_Y->Draw("same");

   float sum_diff_Y = 0;
   for (int i=0; i<h_hits_Y->GetNbinsX();i++)
     {
       float mean= (h_singles_Y->GetBinContent(i) + h_hits_Y->GetBinContent(i))/2;
       if(mean==0) continue;       
       float diff =  fabs(h_singles_Y->GetBinContent(i) - h_hits_Y->GetBinContent(i))/mean ;
       sum_diff_Y += diff;

       // if(h_singles_Y->GetBinContent(i)!=h_hits_Y->GetBinContent(i))
       // cout<<"wrond bin Y "<<h_hits_Y->GetBinCenter(i)<<" "<<h_singles_Y->GetBinCenter(i) <<endl;
     }

   float conclusion_Y = sum_diff_Y/h_hits_Y->GetNbinsY()*100;

   TString* str_Y = new TString(Form("rel. diff = %.2f %c",conclusion_Y,'%'));
   TLatex *myTex_Y = new TLatex(0.25, 0.2, *str_Y);
   myTex_Y->SetNDC();
   myTex_Y->SetTextSize(0.05);
   myTex_Y->Draw();


   

   cc->cd(5);

   h_hits_Z->SetLineWidth(1);
   h_hits_Z->SetLineColor(1);
   h_hits_Z->GetXaxis()->SetTitle("global Z, cm");
   h_hits_Z->GetYaxis()->SetTitleOffset(1.0); 
   h_hits_Z->GetYaxis()->SetTitle("Arbitrary units");
  
   h_hits_Z->Draw();

   h_singles_Z->SetMarkerStyle(2);
   h_singles_Z->SetMarkerColor(2);
   h_singles_Z->SetLineColor(2);
   //h_singles_energy->SetMarkerSize(3);
   h_singles_Z->Draw("same");

   float sum_diff_Z = 0;
   for (int i=0; i<h_hits_Z->GetNbinsX();i++)
     {
       float mean= (h_singles_Z->GetBinContent(i) + h_hits_Z->GetBinContent(i))/2;
       if(mean==0) continue;       
       float diff =  fabs(h_singles_Z->GetBinContent(i) - h_hits_Z->GetBinContent(i))/mean ;
       sum_diff_Z += diff;

       //if(h_singles_Z->GetBinContent(i)!=h_hits_Z->GetBinContent(i))
       // cout<<"wrond bin Z "<<h_hits_Z->GetBinCenter(i)<<" "<<h_singles_Z->GetBinCenter(i) <<endl;
       
     }

   float conclusion_Z = sum_diff_Z/h_hits_Z->GetNbinsZ()*100;

   TString* str_Z = new TString(Form("rel. diff = %.2f %c",conclusion_Z,'%'));
   TLatex *myTex_Z = new TLatex(0.25, 0.2, *str_Z);
   myTex_Z->SetNDC();
   myTex_Z->SetTextSize(0.05);
   myTex_Z->Draw();


   
   /*TLegend* leg = new TLegend(0.295977,0.7774481,0.5905172,0.8635015,NULL,"brNDC");
   leg->SetBorderSize(0);
   leg->SetTextFont(62);
   leg->SetTextSize(0.03560831);
   leg->SetFillColor(0);
   leg->SetFillStyle(1001);
   leg->AddEntry(h_hits_totEdep, "Offline Digi", "l");
   leg->AddEntry(h_singles_energy, "Gate Digi", "p");
   leg->Draw();
   */


   
   //Singles->Draw("energy","","esame");

   // h_totEdep->SetLineWidth(2);
   // h_totEdep->SetLineColor(1);


   

   /*     
//
//Declaration of leaves types - TTree Coincidences
//  
   Int_t           RayleighCrystal1;
   Int_t           RayleighCrystal2;
   Int_t           RayleighPhantom1;
   Int_t           RayleighPhantom2;
   Char_t          RayleighVolName1[40];
   Char_t          RayleighVolName2[40];
   Float_t         axialPos;
   Char_t          comptVolName1[40];
   Char_t          comptVolName2[40];
   Int_t           compton1;
   Int_t           compton2;
   Int_t           crystalID1;
   Int_t           crystalID2;
   Int_t           comptonPhantom1;
   Int_t           comptonPhantom2;
   Float_t         energy1;
   Float_t         energy2;   
   Int_t           eventID1;
   Int_t           eventID2;
   Float_t         globalPosX1;
   Float_t         globalPosX2;
   Float_t         globalPosY1;
   Float_t         globalPosY2;      
   Float_t         globalPosZ1;
   Float_t         globalPosZ2;
   Int_t           layerID1;
   Int_t           layerID2;
   Int_t           moduleID1;
   Int_t           moduleID2;
   Float_t         rotationAngle;
   Int_t           rsectorID1;
   Int_t           rsectorID2;
   Int_t           runID;
   Float_t         sinogramS;
   Float_t         sinogramTheta;
   Int_t           sourceID1;
   Int_t           sourceID2;
   Float_t         sourcePosX1;
   Float_t         sourcePosX2;
   Float_t         sourcePosY1;
   Float_t         sourcePosY2;
   Float_t         sourcePosZ1;
   Float_t         sourcePosZ2;
   Int_t           submoduleID1;
   Int_t           submoduleID2;
   Double_t         time1;
   Double_t         time2;
   
   Float_t         zmin,zmax,z;
//   
//Set branch addresses - TTree Coincicences
//  
   Coincidences->SetBranchAddress("RayleighCrystal1",&RayleighCrystal1);
   Coincidences->SetBranchAddress("RayleighCrystal2",&RayleighCrystal2);
   Coincidences->SetBranchAddress("RayleighPhantom1",&RayleighPhantom1);
   Coincidences->SetBranchAddress("RayleighPhantom2",&RayleighPhantom2);
   Coincidences->SetBranchAddress("RayleighVolName1",&RayleighVolName1);
   Coincidences->SetBranchAddress("RayleighVolName2",&RayleighVolName2);
   Coincidences->SetBranchAddress("axialPos",&axialPos);
   Coincidences->SetBranchAddress("comptVolName1",&comptVolName1);
   Coincidences->SetBranchAddress("comptVolName2",&comptVolName2);
   Coincidences->SetBranchAddress("comptonCrystal1",&compton1);
   Coincidences->SetBranchAddress("comptonCrystal2",&compton2);
   Coincidences->SetBranchAddress("crystalID1",&crystalID1);
   Coincidences->SetBranchAddress("crystalID2",&crystalID2);
   Coincidences->SetBranchAddress("comptonPhantom1",&comptonPhantom1);
   Coincidences->SetBranchAddress("comptonPhantom2",&comptonPhantom2);
   Coincidences->SetBranchAddress("energy1",&energy1);
   Coincidences->SetBranchAddress("energy2",&energy2);   
   Coincidences->SetBranchAddress("eventID1",&eventID1);
   Coincidences->SetBranchAddress("eventID2",&eventID2);
   Coincidences->SetBranchAddress("globalPosX1",&globalPosX1);
   Coincidences->SetBranchAddress("globalPosX2",&globalPosX2);
   Coincidences->SetBranchAddress("globalPosY1",&globalPosY1);
   Coincidences->SetBranchAddress("globalPosY2",&globalPosY2);      
   Coincidences->SetBranchAddress("globalPosZ1",&globalPosZ1);
   Coincidences->SetBranchAddress("globalPosZ2",&globalPosZ2);
   Coincidences->SetBranchAddress("rotationAngle",&rotationAngle);
   Coincidences->SetBranchAddress("runID",&runID);
   Coincidences->SetBranchAddress("sinogramS",&sinogramS);
   Coincidences->SetBranchAddress("sinogramTheta",&sinogramTheta);
   Coincidences->SetBranchAddress("sourceID1",&sourceID1);
   Coincidences->SetBranchAddress("sourceID2",&sourceID2);
   Coincidences->SetBranchAddress("sourcePosX1",&sourcePosX1);
   Coincidences->SetBranchAddress("sourcePosX2",&sourcePosX2);
   Coincidences->SetBranchAddress("sourcePosY1",&sourcePosY1);
   Coincidences->SetBranchAddress("sourcePosY2",&sourcePosY2);
   Coincidences->SetBranchAddress("sourcePosZ1",&sourcePosZ1);
   Coincidences->SetBranchAddress("sourcePosZ2",&sourcePosZ2);
   Coincidences->SetBranchAddress("time1",&time1);
   Coincidences->SetBranchAddress("time2",&time2);
   */ 
  
}	
