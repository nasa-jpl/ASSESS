cd ASSESS/text_analysis  
docker build -t assessimage .  
  
run a docker with ports and volumns:  
docker run -v ./volume:/disk -p 8080:8080 —name assesscontainer -it assessimage  
