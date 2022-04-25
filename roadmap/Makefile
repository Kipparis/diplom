all: graph show

graph: roadmap.dot
	dot -Tpng roadmap.dot -o roadmap.png

show: roadmap.png
	rifle roadmap.png
