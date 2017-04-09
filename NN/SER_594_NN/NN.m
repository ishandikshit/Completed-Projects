function [] = NN(path)

    X_train = loadfile(path, 'input_train.mat');
    y_train = loadfile(path, 'target_train.mat');
    X_test = loadfile(path, 'input_test.mat');
    y_test = loadfile(path, 'target_test.mat');

    net = feedforwardnet(25);
    net = init(net);
    net = train(net,X_train,y_train);

    y_test_predicted = sim(net,X_test);
    y_test_predicted = getclasslabel(y_test_predicted);
    [y_test_predicted,~] = vec2ind(y_test_predicted);
    accuracy = classperf(y_test, y_test_predicted);
    get(accuracy);
    disp('Percentage Accuracy of prediction is: ');
    disp(accuracy.CorrectRate*100);
end

function s = loadfile(folder, file)
    pathplusname = fullfile(folder,  file);
    if ~exist(pathplusname, 'file')
      message = sprintf('%s does not exist', pathplusname);
      uiwait(warndlg(message));
      return;
    else
        s = importdata(pathplusname);
        if ~isempty(strfind(file,'X_'))
            s = s';
        end
      %whos s;
    end
end

function y_test_predicted = getclasslabel(y_test_predicted)
    [x, y] = size(y_test_predicted);

    for j = 1:y
        max = -9999999.00;
        index = 0;
        for i = 1:x
            if y_test_predicted(i,j)>max
                max = y_test_predicted(i,j);
                index = i;
            end
        end
        for i = 1:x
            y_test_predicted(i,j) = 0;
        end
        y_test_predicted(index,j) = 1;
    end
end