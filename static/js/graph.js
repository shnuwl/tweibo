function getData() {
    var uid = document.getElementById("tencentUid").value;
    $.ajax({
            type : "POST",
            url :  '/select_gdata',
            data : {uid : uid},
            dataType : "json",
            success : function(data) {

              function Topology(ele){
                  typeof(ele)=='string' && (ele=document.getElementById(ele));
                  var w=ele.clientWidth,
                      h=ele.clientHeight,
                      self=this;
                  this.force = d3.layout.force().gravity(.05).distance(200).charge(-800).size([w, h]);
                  this.nodes=this.force.nodes();
                  this.links=this.force.links();
                  this.clickFn=function(){};
                  this.vis = d3.select(ele).append("svg:svg")
                               .attr("width", w).attr("height", h).attr("pointer-events", "all");

                  this.force.on("tick", function(x) {
                    self.vis.selectAll("g.node")
                        .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });

                    self.vis.selectAll("line.link")
                        .attr("x1", function(d) { return d.source.x; })
                        .attr("y1", function(d) { return d.source.y; })
                        .attr("x2", function(d) { return d.target.x; })
                        .attr("y2", function(d) { return d.target.y; });
                  });
              }


              Topology.prototype.doZoom=function(){
                  d3.select(this).select('g').attr("transform","translate(" + d3.event.translate + ")"+ " scale(" + d3.event.scale + ")");

              }


              //增加节点
              Topology.prototype.addNode=function(node){
                  this.nodes.push(node);
              }

              Topology.prototype.addNodes=function(nodes){
                  if (Object.prototype.toString.call(nodes)=='[object Array]' ){
                      var self=this;
                      nodes.forEach(function(node){
                          self.addNode(node);
                      });

                  }
              }

              //增加连线
              Topology.prototype.addLink=function(source,target){
                  this.links.push({source:this.findNode(source),target:this.findNode(target)});
              }

              //增加多个连线
              Topology.prototype.addLinks=function(links){
                  if (Object.prototype.toString.call(links)=='[object Array]' ){
                      var self=this;
                      links.forEach(function(link){
                          self.addLink(link['source'],link['target']);
                      });
                  }
              }
              //删除节点
              Topology.prototype.removeNode=function(id){
                  var i=0,
                      n=this.findNode(id),
                      links=this.links;
                  while ( i < links.length){
                      links[i]['source']==n || links[i]['target'] ==n ? links.splice(i,1) : ++i;
                  }
                  this.nodes.splice(this.findNodeIndex(id),1);
              }

              //删除节点下的子节点，同时清除link信息
              Topology.prototype.removeChildNodes=function(id){
                  var node=this.findNode(id),
                      nodes=this.nodes;
                      links=this.links,
                      self=this;

                  var linksToDelete=[],
                      childNodes=[];
                  
                  links.forEach(function(link,index){
                      link['source']==node 
                          && linksToDelete.push(index) 
                          && childNodes.push(link['target']);
                  });

                  linksToDelete.reverse().forEach(function(index){
                      links.splice(index,1);
                  });

                  var remove=function(node){
                      var length=links.length;
                      for(var i=length-1;i>=0;i--){
                          if (links[i]['source'] == node ){
                             var target=links[i]['target'];
                             links.splice(i,1);
                             nodes.splice(self.findNodeIndex(node.id),1);
                             remove(target);
                             
                          }
                      }
                  }

                  childNodes.forEach(function(node){
                      remove(node);
                  });

                  //清除没有连线的节点
                  for(var i=nodes.length-1;i>=0;i--){
                      var haveFoundNode=false;
                      for(var j=0,l=links.length;j<l;j++){
                          ( links[j]['source']==nodes[i] || links[j]['target']==nodes[i] ) && (haveFoundNode=true) 
                      }
                      !haveFoundNode && nodes.splice(i,1);
                  }
              }

              //查找节点
              Topology.prototype.findNode=function(id){
                  var nodes=this.nodes;
                  for (var i in nodes){
                      if (nodes[i]['id']==id ) return nodes[i];
                  }
                  return null;
              }


              //查找节点所在索引号
              Topology.prototype.findNodeIndex=function(id){
                  var nodes=this.nodes;
                  for (var i in nodes){
                      if (nodes[i]['id']==id ) return i;
                  }
                  return -1;
              }

              //节点点击事件
              Topology.prototype.setNodeClickFn=function(callback){
                  this.clickFn=callback;
              }

              //更新拓扑图状态信息
              Topology.prototype.update=function(){
                var link = this.vis.selectAll("line.link")
                    .data(this.links)
                    .attr("class", function(d){
                          return 'link';
                    });


                link.enter().insert("svg:line", "g.node")
                    .attr("class", function(d){
                       return 'link';
                    });

                link.exit().remove();

                var node = this.vis.selectAll("g.node")
                    .data(this.nodes);

                var nodeEnter = node.enter().append("svg:g")
                    .attr("class", "node")
                    .call(this.force.drag);

                //根据节点的影响力确定节点的半径大小
                var self=this;
                nodeEnter.append("svg:circle")
                    .attr("class", "node")
                    .attr("r",  function(d){
                        if(d.count<=2){
                          return 8;
                        }else if(d.count>2){
                          return 10;
                        }else{
                          return 5;
                        }
                    })
                    .style("fill", function(d) {
                      if(d.attitude==1){
                        return color("#292929");
                      }else if(d.attitude==0){
                        return color("#e7ba52");
                      }else if(d.attitude==-1){
                        return color("#ad494a");
                      }else{
                        return color(d.count+"");
                      }
                    })
                    .on('dblclick',function(d){ d.expand && self.clickFn(d);})
                    .on('mouseover',function(d) { id="#"+d.id,$(id).css('display','inline'); });

                nodeEnter.append("svg:text")
                    .attr("class", "nodetext")
                    .attr("dx", 5)
                    .attr("dy", -15)
                    .text(function(d) { return d.id });

                nodeEnter.append("svg:text")
                    .attr("class","texts")
                    .attr("id", function(d) { return d.id })
                    .attr("dx", 15)
                    .attr("dy", -35)
                    .attr("style","display:none")
                    .text(function(d) { return d.text });

                node.exit().remove();

                this.force.start();
              }




              var topology=new Topology('container');

              var nodes=data.nodes;
              // [
              //     {id:'10.4.42.1',type:'router',status:1},
              //     {id:'10.4.43.1',type:'switch',status:1,expand:true},
              //     {id:'10.4.44.1',type:'switch',status:1},
              //     {id:'10.4.45.1',type:'switch',status:0}

              // ];

              var childNodes=data.childNodes;
              alert(data);
              // [
              //     {id:'10.4.43.2',type:'switch',status:1},
              //     {id:'10.4.43.3',type:'switch',status:1}

              // ];

              var links=data.links;
              // [
              //     {source:'10.4.42.1',target:'10.4.43.1'},
              //     {source:'10.4.42.1',target:'10.4.44.1'},
              //     {source:'10.4.42.1',target:'10.4.45.1'}
              // ];

              var childLinks=data.childLinks;
              // [
              //     {source:'10.4.43.1',target:'10.4.43.2'},
              //     {source:'10.4.43.1',target:'10.4.45.1'},
              //     {source:'10.4.43.1',target:'10.4.43.3'},
              //     {source:'10.4.43.2',target:'10.4.43.3'}
              // ]
              var color = d3.scale.category20();

              topology.addNodes(nodes);
              topology.addLinks(links);
              //可展开节点的点击事件
              topology.setNodeClickFn(function(node){
                  if(!node['_expanded']){
                      expandNode(node.id);
                      node['_expanded']=true;
                  }else{
                      collapseNode(node.id);
                      node['_expanded']=false;
                  }
              });
              topology.update();


              function expandNode(id){
                  topology.addNodes(childNodes);
                  topology.addLinks(childLinks);
                  topology.update();
              }

              function collapseNode(id){
                  topology.update();
              }
            }
    });
}