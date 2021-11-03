close all; clc


precision = [];
recall = [];
f1score = [];
% load('vertices.mat')
% load('edges.mat')
edges = [];

%%%% give the path to g2o file to read in MATLAB
fileID = fopen('g2o_files_dataset/intel/intel_false_LS.g2o','r');
while true
    thisline = fgetl(fileID);
    if ~ischar(thisline); break; end
    str = split(thisline, ' ');
    temp = [];
    if strcmp(str{1}, 'EDGE_SE2')
        for i = 2:length(str)
            temp = [temp str2num(str{i})];
        end
        edges = [edges; temp];
    end
end
fclose(fileID);

pg = poseGraph;
 
% for i = 2:length(vertices)
%     addRelativePose(pg, vertices(i, 2:end));    
% end

for i = 1:length(edges)
    addRelativePose(pg, edges(i, 3:5), edges(i, 6:end), edges(i, 1)+1, edges(i, 2)+1);
end

IDs = 1:length(edges);
edges = [IDs' edges];

TotalLCs = pg.LoopClosureEdgeIDs;

TrueLCs = 0;
FalseLCs = 0;

for i = 1:length(TotalLCs)
    temp = TotalLCs(i);
    tempedge = edges(temp, :);
    if sum(tempedge(4:6) ~= 0) ~= 0
        TrueLCs = TrueLCs + 1;
    else
        FalseLCs = FalseLCs + 1;
    end     
end


threshold = 15;

for k = 1:length(threshold)
    
trimParams.MaxIterations = 100;
trimParams.TruncationThreshold = threshold(k);

solverOptions = poseGraphSolverOptions;
[pgNew, trimInfo, debugInfo] = trimLoopClosures(pg, trimParams, solverOptions);

removedLCs = trimInfo.LoopClosuresToRemove;

removedTrueLCs = 0;
removedFalseLCs = 0;

for i = 1:length(removedLCs)
    temp = removedLCs(i);
    tempedge = edges(temp, :);
    if sum(tempedge(4:6) ~= 0) ~= 0
        removedTrueLCs = removedTrueLCs + 1;
    else
        removedFalseLCs = removedFalseLCs + 1;
    end     
end

truePositive = TrueLCs - removedTrueLCs;
trueNegative = removedFalseLCs;
falsePositive = FalseLCs - removedFalseLCs;
falseNegative = removedTrueLCs;

tempPrecision = truePositive/(truePositive + falsePositive);
precision = [precision, tempPrecision];
tempRecall = truePositive/(truePositive + falseNegative);
recall = [recall, tempRecall];

f1score = [f1score, 2*tempPrecision*tempRecall/(tempPrecision + tempRecall)];

% hold on
% plot(removedLCs, zeros(length(removedLCs)), 'or')
% title('Edge Residual Errors and Removed Loop Closures')
% legend('Residual Errors', 'Removed Loop Closures')
% xlabel('Edge IDs')
% ylabel('Edge Residual Error')
% hold off
% 
figure
title('new pose graph optimized')
show(pgNew, "IDs", "off");
% k
% plot(recall, precision)
% title('Precision-Recall curve')
% xlabel('Recall')
% ylabel('Precision')
end


% optimizedPoseGraphINTEL = optimizePoseGraph(pgNew);
% figure
% show(optimizedPoseGraphINTEL,'IDs','off');