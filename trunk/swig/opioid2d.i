%module(directors="1") cOpioid2D
%include "std_string.i"
%include "std_vector.i"
%include "std_list.i"
%{
#include "opioid2d.hpp"
#include "singleton.hpp"
%}
%nodefaultctor;
%feature("director") SceneCallbacks;
%feature("director") DeleteCallback;
%feature("director") ActionCallbacks;

//typedef double floatval;
typedef float floatval;

typedef unsigned short Uint8;

namespace opi2d
{
	class Node;
	class Sprite;
	class Layer;
}

%template(LayerList) std::list<opi2d::Layer*>;
%template(NodeList) std::list<opi2d::Node*>;
%template(SpriteList) std::vector<opi2d::Sprite*>;


namespace opi2d
{

void InitOpioid2D();
void QuitOpioid2D();

%include "o2d_util.i"
%include "o2d_image.i"
%include "o2d_actions.i"
%include "o2d_node.i"
%include "o2d_particles.i"
%include "o2d_scene.i"
%include "o2d_sprite.i"
%include "o2d_area.i"
%include "o2d_mutators.i"
%include "o2d_singletons.i"
%include "o2d_vm.i"

}
