/*
 * Opioid2D - camera
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * Defines the Camera class used in scenes. See scene.hpp for more
 * details.
 */
#ifndef OPICAMERA
#define OPICAMERA

#include "util.hpp"
#include "node.hpp"
#include "vec.hpp"

namespace opi2d
{
	class Layer;
	
	/*
	 * The camera functionality is a work-in-progress. Currently the Camera
	 * object is a standard Node, and all functionality is implemented in the
	 * Scene class.
	 * 
	 * This is due to change in the future.
	 */ 
    class Camera : public Node
    {
    	public:
    	
    	Camera();
    	
    	// convert screen coordinates to world coordinates
    	void ScreenToWorld(Vec2& p) const;
    	void ScreenToWorld(Vec2& p, Layer* layer) const;
    	
    	void Adjust();    	
    	void SetAlign(bool flag);
    	bool GetAlign() const;
    	
    	protected:
    	
    	bool alignToParent;
    };
}

#endif

