means = csvread('mean_by_cost',1,0);
means = means(:,[1 8 4 3 6 7 5]);

errs = csvread('error_by_cost',1,0);
errs = errs(:,[1 8 4 3 6 7 5]);

fig = figure();
ax = axes;
hold on;

myColorOrder = [[0.4660 0.6740 0.1880];[0.8500 0.3250 0.0980];[0 0.4470 0.7410];[0.9290 0.6940 0.1250];[0.4940 0.1840 0.5560];[0.6350 0.0780 0.1840]];
nbars = size(means, 2)-1;

for i = 1:nbars
    errorbar(means(:,1), means(:,i+1), errs(:,i+1), 'LineWidth',3, 'Color',myColorOrder(i,:));
end

% set(gca, 'ColorOrder', myColorOrder, 'NextPlot', 'replacechildren');

% X and Y labels
xlabel ('Cost');
ylabel ('Metareasoning Performance');
ylim([0.4,0.8]);
box on
set(gca,'FontSize',16,'XScale','log')

lg = legend('Optimal', 'Blinkered', 'BMPS', 'Full Deliberation', 'Meta-greedy','DQN');
lg.Location = 'Northeast';