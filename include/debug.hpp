/*
 * Opioid2D - debug
 * Copyright (c) 2006 Sami Hangaslammi <shang@iki.fi>
 * 
 * Utility macros and functions for debugging output
 * 
 */

#ifndef OPIDEBUG
#define OPIDEBUG
#ifdef DEBUGGING
void debugout(const char* file, int line, const char* str);
void debugout(const char* file, int line, int i);
#define DEBUG(msg) debugout(__FILE__, __LINE__, msg)
#define FUNC debugout(__FILE__, __LINE__, __FUNCTION__);
#else
#define DEBUG(msg)
#define FUNC
#endif
#endif

