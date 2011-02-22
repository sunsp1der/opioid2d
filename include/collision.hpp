/*
 * Opioid2D - collision
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * Defines the classes for collision nodes. Each image can have zero, one or several
 * nodes that are used to check for collisions.
 * 
 * The actual collision logic is part of the Scene class at the moment, but might
 * get moved to this module in the future.
 */
#ifndef OPICOLLISION
#define OPICOLLISION

#include "util.hpp"

#include <vector>
#include <cmath>

#include "vec.hpp"

namespace opi2d
{
	/*
	 * Currently, collision nodes are restricted to rectangle shape. In a later implementation
	 * each collision node will be a convex polygon (the interface stays the same).
	 */ 
	struct CollisionNode
	{
		Vec2 center;
		Vec2 size;
		
		CollisionNode(const CollisionNode& x) : center(x.center), size(x.size) {}
		
		CollisionNode(floatval x, floatval y, floatval width, floatval height)
		{
			width *= 0.5;
			height *= 0.5;
			center.set(x+width, y+height);
			// this is not an error, size actually contains the half-size, because that's faster in calculations
			size.set(width, height);
		}
		
		bool CheckOverlap(const CollisionNode &other) const
		{
			return (fabs(center.x-other.center.x) < size.x+other.size.x) && (fabs(center.y-other.center.y) < size.y+other.size.y);			
		}
	};
	
    typedef std::vector<CollisionNode> CollisionNodes;

}

#endif

