
int plotterWidth = 104; //maximum width of plot matrix.
int plotterHeight = 104; //maximum height of plot matrix.

PImage img; // image to be plotted
/*---->*/String plotImageFile = "me.jpg";//filename of image to be plotted (name and extension if in this directory, otherwise full path).

PrintWriter outFil;
/*---->*/String plotDataFile = "plotMatrix.txt"; //filename and path to which the plot matrix will be saved (if no path, then in this directory).

void setup(){
  img = loadImage(plotImageFile);
  outFil = createWriter(plotDataFile);
  size(500, 400);
  noLoop();
}

void draw(){
  resizeImage();
  filterImage();
  image(img, 0, 0);
  generatePlotMatrix();
}



//-------------- Low Level Method Implementation -----------------
void resizeImage(){
  if(img.width > img.height){
    //landscape picture, then rotate it by 90 degrees.
    img = rotateImg();
  }
  img.resize(plotterWidth, 0);
  if(img.height > plotterHeight){
    img.resize(0, plotterHeight);
  }
}

void filterImage(){
  img.filter(GRAY);
  img.filter(POSTERIZE, 3);
}

void generatePlotMatrix(){
  img.loadPixels();
  for(int y = 0; y < img.height; y++){
    
    outFil.print("{");
    for(int x = 0; x < img.width; x++){
      int curr = (y * img.width) + x;
      int pixelShade = (int)red(img.pixels[curr]);
      int plotShade;
      //char plotShade; //@@##oo**__ to be used to generate ascii images.
      switch(pixelShade){
        case 0:
          plotShade = 2;
          break;
        case 63:
          plotShade = 3;
          break;
        case 127:
          plotShade = 1;
          break;
        case 191:
          plotShade = 1;
          break;
        case 255:
          plotShade = 0;
          break;
        default:
          plotShade = 999;
      }
      outFil.print(plotShade + ",");
    }
    outFil.println("},"); 
  }
  outFil.flush();
  outFil.close();
}

PImage rotateImg(){
  img.loadPixels();
  PImage rotImg = createImage(img.height, img.width, RGB);
  rotImg.loadPixels();
  
  for(int y = 0; y < img.height; y++){
    for(int x = 0; x < img.width; x++){
      rotImg.pixels[(x*rotImg.width) + y] = img.pixels[(y*img.width) + x];
    }
  }
  
  img.updatePixels();
  rotImg.updatePixels();
  return rotImg;
}