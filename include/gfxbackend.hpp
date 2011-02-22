/*
 * Opioid2D - gfxbackend
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * This is an abstract interface for a display backend. It is still a work
 * in progress, but it will be used in the future to make it possible to support
 * several rendering backends (such as OpenGL and DirectX).
 */

#ifndef OPIGFXBACKEND_HPP
#define OPIGFXBACKEND_HPP

namespace opi2d
{
	class GFXBackEnd
	{
		public:
		
		void Initialize();
		void SetOrthogonal();
		
	};
	
	
}

#endif