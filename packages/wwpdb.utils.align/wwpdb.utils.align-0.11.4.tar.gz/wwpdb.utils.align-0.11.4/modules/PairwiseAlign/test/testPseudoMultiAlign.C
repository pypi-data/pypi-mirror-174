#include <stdio.h>
#include <stdlib.h>

#include "PseudoMultiAlign.h"

#define NUM_A 30
static const char *seq_a[NUM_A] = { "A", "A", "A", "G", "C", "A", "A", "G", "C", "G", "G", "G", "C", "C", "G", "C", "A", "C", "G", "C", "G",
                                    "G", "C", "C", "C", "G", "C", "A", "A", "A" };
static const char *idx_a[NUM_A] = { "0", "1", "2", "3", "4", "5", "6", "7", "8", "9","10","11","12","13","14","15","16","17","18","19","20",
                                   "21","22","23","24","25","26","27","28","29" };
#define NUM_B 17
static const char *seq_b[NUM_B] = { "A", "A", "A", "G", "C", "A", "G", "C", "G", "G", "C", "C", "G", "C", "A", "A", "A" };
static const char *idx_b[NUM_B] = { "0", "1", "2", "3", "4", "5", "6", "7", "8", "9","10","11","12","13","14","15","16" };
static const char *links[NUM_B] = { "1", "1", "1", "1", "1", "0", "1", "1", "1", "0", "1", "1", "1", "1", "1", "1", "1" };
static const char *numbs[NUM_B] = {  "648", "649", "650", "651", "652", "652A", "652C", "652D", "652E", "652F", "652S", "652T", "652U", "652V",
                                     "653", "654", "655" };

using namespace RCSB;

int main(int argc, char *argv[])
{
       std::vector<std::string> data;
       std::vector<std::vector<std::string> > authSeqs, coordSeqs;

       authSeqs.clear();
       for (int i = 0; i < NUM_A; ++i) {
            data.clear();
            data.push_back(seq_a[i]);
            data.push_back(idx_a[i]);
            authSeqs.push_back(data);
       }
       coordSeqs.clear();
       for (int i = 0; i < NUM_B; ++i) {
            data.clear();
            data.push_back(seq_b[i]);
            data.push_back(idx_b[i]);
            data.push_back(links[i]);
            data.push_back(numbs[i]);
            coordSeqs.push_back(data);
       }

       PseudoMultiAlign pa = PseudoMultiAlign();
       pa.setAuthSequence(authSeqs);
       pa.addAlignSequence(coordSeqs);

       std::vector<std::vector<int> > idxList = pa.getAlignIndices();
       for (unsigned int i = 0; i < idxList.size(); ++i) {
            for (unsigned int j = 0; j < idxList[i].size(); ++j) printf(" %6d", idxList[i][j]);
            printf("\n");
       }

       return 0;
}

