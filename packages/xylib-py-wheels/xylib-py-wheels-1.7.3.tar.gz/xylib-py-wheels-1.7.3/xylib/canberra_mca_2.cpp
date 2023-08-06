//Alternate Canberra MCA File format
//If anyone can combine this with the existing one feel free but I couldn't - CS
#define BUILDING_XYLIB
#include "canberra_mca_2.h"

#include <ctime>
#include <cstring>

#include "util.h"

using namespace std;
using namespace xylib::util;

namespace xylib {


const FormatInfo CanberraMca2DataSet::fmt_info(
    "canberra_mca_2",
    "Canberra MCA",
    "mca",
    true,                       // whether binary
    false,                      // whether has multi-blocks
    &CanberraMca2DataSet::ctor,
    &CanberraMca2DataSet::check
);

bool CanberraMca2DataSet::check(istream &f, string*)
{
    int head = read_uint32_le(f);
    return head == 196608;
}

static
string get_time(int t){
    time_t rawtime = (time_t)t;
    char s[64];
    int r = strftime(s, sizeof(s), "%a, %Y-%m-%d %H:%M:%S", gmtime(&rawtime));
    return s;
}

void CanberraMca2DataSet::load_data(std::istream &f, const char*)
{
    AutoPtrBlock blk(new Block);
    Column *xcol = NULL;
    VecColumn *ycol = new VecColumn;

    f.seekg(0, f.beg);
    f.ignore(38);
    int startTime = read_uint32_le(f);
    blk->meta["Start Time"] = get_time(startTime);

    f.ignore(6);
    int livetime = read_uint32_le(f);
    int realtime = read_uint32_le(f);
    blk->meta["live time (s)"] = std::to_string(livetime);
    blk->meta["real time (s)"] = std::to_string(realtime);

    f.ignore(16);
    float slope = read_flt_le(f);
    float intercept = read_flt_le(f);

    f.ignore(46);
    int count = read_int16_le(f);
    xcol = new StepColumn(intercept, slope, count);

    for(int i=0;i<count;i++){
        if(f.eof()){
            break;
        }
        int yval = read_uint32_le(f);
        ycol->add_val(yval);
    }

    blk->add_column(xcol);
    blk->add_column(ycol);
    add_block(blk.release());
} 
}// namespace xylib