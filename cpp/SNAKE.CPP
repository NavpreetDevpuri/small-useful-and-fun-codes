 #include<stdio.h>
 #include<iostream.h>
 #include<conio.h>
 #include<dos.h>
 #include<stack.h>
 #include<process.h>
 #include<stdlib.h>
 class snake{
  public:
  int i,j,n,sn[999][2],k,l,e,*m,s,p,f,ai,aj,*sc,t,go;
  snake(){
   sn[0][0]=12;
   sn[0][1]=14;
   sn[1][0]=12;
   sn[1][1]=13;
   sn[2][0]=12;
   sn[2][1]=12;
   sn[0][0]=12;
   sn[0][1]=14;
   n=3;
   p=0;
   f=0;
   ai=6;
   *sc=0;
   aj=15;
   go=1;
  }
  void run(){
  int ti,tj,tei,tej;
  ti=sn[0][0];
  tj=sn[0][1];
  *m=*m+(s*1);
    for(i=1;i<n;++i){
     tei=ti;
     tej=tj;
     ti=sn[i][0];
     tj=sn[i][1];
     sn[i][0]=tei;
     sn[i][1]=tej;
    }
  }

  void control(){
   if(kbhit()){
   p=1;
   char c = getch();
   if((c==72||c==119)&&t%2!=0){
    m=&sn[0][0];
    s=-1;
    t=2;
   }else if((c==97||c==75)&&t%2==0){
    m=&sn[0][1];
    s=-1;
    t=1;
   }else if((c==80||c==115)&&t%2!=0){
    m=&sn[0][0];
    s=1;
    t=4;
   }else if((c==77||c==100)&&t%2==0){
     m=&sn[0][1];
     s=1;
     t=3;
   }else if(c=='e'){
     exit(1);
     exit(1);
   }
  }
 }
 void isout(){
  if(sn[0][0]<4||sn[0][0]>21||sn[0][1]<2||sn[0][1]>37){
    go=0;
  }
  for(i=1;i<n;++i){
   if(sn[i][0]==sn[0][0]&&sn[i][1]==sn[0][1]){
    go=0;
   }
  }

 }
 void display(){
  clrscr();
  for(i=0;i<24;++i){
   if(i!=1){
   for(j=0;j<40;++j){
   if(i==ai&&j==aj){
    if(sn[0][0]==ai&&sn[0][1]==aj){
       ai=4+random(18);
       aj=3+random(35);
       ++n;
       ++*sc;
      }
    char c=232;
     cout<<c<<c;
   }else{
    if(i<4||i>21||j<2||j>37){
     char c=219;
     cout<<c<<c;
    }
    else{
    e=0;
     for(k=0;k<n;++k){
      if(sn[k][0]==i&&sn[k][1]==j){
       e=1;
       break;
      }
    }
    if(e==1){
     char c=176;
     if(k==0){
      c=178;
     }
     cout<<c<<c;
    }else{
     cout<<"  ";
    }
   }}
  }}else{
    cout<<"                                                            Score : ("<<*sc<<")"<<endl;
  }
 }

 }
};
 void main(){
  snake s;
  s.display();
  s.m=&s.sn[0][1];
  s.s=1;
  s.t=3;
  while(s.go){
   s.control();
   s.run();
   s.isout();
   s.display();
   delay(123);
  }
 cout<<"                          Game Over, Your Score is "<<*s.sc;
 getch();
 }